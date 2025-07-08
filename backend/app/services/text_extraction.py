"""
Text extraction service for Manim code.
This module extracts narration text from Manim code.
"""
import re
import logging
from typing import List, Dict, Any

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ManimTextExtractor:
    """
    Extracts narration text from Manim code.
    """
    
    def __init__(self):
        # Regular expressions for extracting text
        self.text_object_pattern = re.compile(r'Text\s*\(\s*["\']([^"\']+)["\']')
        self.mathtex_pattern = re.compile(r'MathTex\s*\(\s*r?["\']([^"\']+)["\']')
        self.tex_pattern = re.compile(r'Tex\s*\(\s*r?["\']([^"\']+)["\']')
        self.title_pattern = re.compile(r'Title\s*\(\s*["\']([^"\']+)["\']')
        
        # Pattern to extract wait times
        self.wait_pattern = re.compile(r'self\.wait\s*\(\s*(\d+\.?\d*)\s*\)')
        
        # Pattern to extract run_time from play commands
        self.run_time_pattern = re.compile(r'self\.play\s*\([^)]*run_time\s*=\s*(\d+\.?\d*)')
        
        # Pattern to extract NARRATION comments
        # Find lines starting with "# NARRATION:" and possibly continuing with lines starting with "#"
        self.narration_line_pattern = re.compile(r'^\s*#\s*NARRATION:\s*(.+)$', re.MULTILINE | re.IGNORECASE)
        self.continuation_line_pattern = re.compile(r'^\s*#\s*([^N].+)$', re.MULTILINE)
        
        # Default timing values (in seconds)
        self.default_wait_time = 2.0
        self.default_animation_time = 1.5
        
    def extract_script(self, manim_code: str) -> List[Dict[str, Any]]:
       
        # Try to extract NARRATION comments first (highest priority)
        script = self._extract_narration_comments(manim_code)
        
        # If no NARRATION comments found, try to extract section comments
        if not script:
            script = self._extract_section_comments(manim_code)
        
        # If no sections found, try to extract text objects
        if not script:
            script = self._extract_text_objects(manim_code)
        
        # If still no script, extract any comments
        if not script:
            script = self._extract_general_comments(manim_code)
        
        return script
    
    def _extract_narration_comments(self, manim_code: str) -> List[Dict[str, Any]]:
        """
        Extract script from NARRATION comments in the code.
        
        This method looks for comments starting with "# NARRATION:" and extracts
        the continuous block of comments that follows.
        
        Args:
            manim_code: The Manim code to extract from
            
        Returns:
            List of script segments
        """
        script = []
        current_time = 0.0
        
        # Split the code into lines
        lines = manim_code.split('\n')
        
        # Find all narration comments
        narration_blocks = []
        current_narration = None
        
        for i, line in enumerate(lines):
            # Check if this line starts a new narration block
            narration_match = re.match(r'^\s*#\s*NARRATION:\s*(.+)$', line, re.IGNORECASE)
            if narration_match:
                # If we were collecting a narration block, save it before starting a new one
                if current_narration is not None:
                    narration_blocks.append(current_narration.strip())
                
                # Start a new narration block
                current_narration = narration_match.group(1).strip()
            
            # Check if this line is a continuation of the current narration block
            elif current_narration is not None and re.match(r'^\s*#\s*(.+)$', line):
                # Extract the comment content without the # prefix
                comment_content = re.match(r'^\s*#\s*(.+)$', line).group(1).strip()
                
                # Ignore comments that start another section or are empty
                if not comment_content.startswith('NARRATION:') and comment_content:
                    current_narration += " " + comment_content
            
            # If we hit a non-comment line and were collecting a narration, save it
            elif current_narration is not None:
                narration_blocks.append(current_narration.strip())
                current_narration = None
        
        # Don't forget to save the last narration block if there is one
        if current_narration is not None:
            narration_blocks.append(current_narration.strip())
        
        # If no NARRATION comments found, return empty script
        if not narration_blocks:
            logger.info("No NARRATION comments found in the code")
            return []
        
        logger.info(f"Found {len(narration_blocks)} NARRATION comment blocks")
        for i, block in enumerate(narration_blocks[:3]):  # Print the first 3 blocks for debugging
            logger.info(f"  Block {i+1}: {block[:50]}..." if len(block) > 50 else f"  Block {i+1}: {block}")
        
        # Extract all wait times to estimate total duration
        wait_times = self.wait_pattern.findall(manim_code)
        total_wait_time = sum(float(t) for t in wait_times) if wait_times else self.default_wait_time * len(narration_blocks)
        
        # Distribute the wait time among the narration blocks
        segment_duration = total_wait_time / len(narration_blocks) if narration_blocks else self.default_animation_time
        
        # Create script segments for each narration block
        for narration in narration_blocks:
            script.append({
                "text": narration,
                "timing": {
                    "start": current_time,
                    "duration": segment_duration
                },
                "type": "narration"
            })
            current_time += segment_duration
        
        return script
    
    def _extract_section_comments(self, manim_code: str) -> List[Dict[str, Any]]:
        """
        Extract script from section comments in the code.
        
        Args:
            manim_code: The Manim code to extract from
            
        Returns:
            List of script segments
        """
        script = []
        current_time = 0.0
        
        # Extract section comments (# 1. Introduction, # 2. Concept, etc.)
        section_pattern = re.compile(r'#\s*(\d+\.\s*[^#\n]+)')
        sections = []
        
        # Find all section comments
        for match in section_pattern.finditer(manim_code):
            section_title = match.group(1)
            start_pos = match.start()
            sections.append((start_pos, section_title))
        
        # Sort sections by position in code
        sections.sort(key=lambda x: x[0])
        
        # If no sections found, return empty script
        if not sections:
            return []
        
        # Process each section
        for i, (pos, section_title) in enumerate(sections):
            # Determine the end position of this section
            end_pos = sections[i+1][0] if i < len(sections) - 1 else len(manim_code)
            
            # Extract the code for this section
            section_code = manim_code[pos:end_pos]
            
            # Create a script segment for the section title
            script.append({
                "text": section_title.strip(),
                "timing": {
                    "start": current_time,
                    "duration": 3.0  # Default duration for section titles
                },
                "type": "section_title"
            })
            current_time += 3.0
            
            # Extract text objects in this section
            text_objects = self.text_object_pattern.findall(section_code)
            
            # Extract wait times in this section
            wait_times = self.wait_pattern.findall(section_code)
            total_wait_time = sum(float(t) for t in wait_times) if wait_times else self.default_wait_time * 2
            
            # If we found text objects, create script segments for them
            if text_objects:
                # Distribute the wait time among the text objects
                segment_duration = total_wait_time / len(text_objects)
                
                for text in text_objects:
                    script.append({
                        "text": text,
                        "timing": {
                            "start": current_time,
                            "duration": segment_duration
                        },
                        "type": "text_object"
                    })
                    current_time += segment_duration
            else:
                # If no text objects, just advance the time
                current_time += total_wait_time
        
        return script
    
    def _extract_text_objects(self, manim_code: str) -> List[Dict[str, Any]]:
        """
        Extract script from text objects in the code.
        
        Args:
            manim_code: The Manim code to extract from
            
        Returns:
            List of script segments
        """
        script = []
        current_time = 0.0
        
        # Extract all text objects
        text_objects = self.text_object_pattern.findall(manim_code)
        
        # Extract all wait times
        wait_times = self.wait_pattern.findall(manim_code)
        total_wait_time = sum(float(t) for t in wait_times) if wait_times else self.default_wait_time * len(text_objects)
        
        # If we found text objects, create script segments for them
        if text_objects:
            # Distribute the wait time among the text objects
            segment_duration = total_wait_time / len(text_objects) if text_objects else self.default_animation_time
            
            for text in text_objects:
                script.append({
                    "text": text,
                    "timing": {
                        "start": current_time,
                        "duration": segment_duration
                    },
                    "type": "text_object"
                })
                current_time += segment_duration
        
        return script
    
    def _extract_general_comments(self, manim_code: str) -> List[Dict[str, Any]]:
        """
        Extract script from general comments in the code.
        
        Args:
            manim_code: The Manim code to extract from
            
        Returns:
            List of script segments
        """
        script = []
        current_time = 0.0
        
        # Extract all comments that are not section comments
        # Look for comments that are not empty and don't start with a number followed by a dot
        comment_pattern = re.compile(r'#\s*(?!\d+\.\s*)([^\n#]+)')
        comments = []
        
        # Find all comments
        for match in comment_pattern.finditer(manim_code):
            comment = match.group(1).strip()
            if comment and len(comment) > 5:  # Skip very short comments
                comments.append(comment)
        
        # Extract all wait times
        wait_times = self.wait_pattern.findall(manim_code)
        total_wait_time = sum(float(t) for t in wait_times) if wait_times else self.default_wait_time * len(comments)
        
        # If we found comments, create script segments for them
        if comments:
            # Distribute the wait time among the comments
            segment_duration = total_wait_time / len(comments) if comments else self.default_animation_time
            
            for comment in comments:
                script.append({
                    "text": comment,
                    "timing": {
                        "start": current_time,
                        "duration": segment_duration
                    },
                    "type": "comment"
                })
                current_time += segment_duration
        
        return script

def extract_narration_script(manim_code: str) -> List[Dict[str, Any]]:
    """
    Extract narration script from Manim code.
    This is the main entry point for extracting narration from Manim code.
    
    Args:
        manim_code: The Manim code to extract from
        
    Returns:
        List of script segments with text and timing information
    """
    logger.info("Extracting narration script from Manim code")
    return extract_narration_from_manim(manim_code)

def extract_narration_from_manim(manim_code: str) -> List[Dict[str, Any]]:
    """
    Extract narration script from Manim code.
    
    Args:
        manim_code: The Manim code to extract from
        
    Returns:
        List of script segments with text and timing information
    """
    extractor = ManimTextExtractor()
    script = extractor.extract_script(manim_code)
    
    # If no script was extracted, create a generic one
    if not script:
        logger.warning("No script could be extracted, creating a generic one")
        script = [{
            "text": "Welcome to this educational video created with Manim.",
            "timing": {
                "start": 0.0,
                "duration": 3.0
            },
            "type": "generic"
        }]
    
    logger.info(f"Extracted {len(script)} narration segments")
    return script
