"""
ElevenLabs Text-to-Speech service for generating narration audio.
"""
import os
import logging
import traceback
from typing import Optional, Dict, Any, List
from pathlib import Path
import asyncio
import time

from elevenlabs import generate, save, set_api_key
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Configure the ElevenLabs API
try:
    ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")
    if not ELEVENLABS_API_KEY:
        logger.warning("ELEVENLABS_API_KEY not found in environment variables")
        logger.warning("Please run 'python setup_env.py' to set up your API key")
    else:
        set_api_key(ELEVENLABS_API_KEY)
        logger.info("ElevenLabs API configured successfully")
except Exception as e:
    logger.error(f"Error configuring ElevenLabs API: {str(e)}")

# Default voice settings
DEFAULT_VOICE_ID = "EXAVITQu4vr4xnSDxMaL"  # Example: "Rachel" voice
DEFAULT_MODEL_ID = "eleven_multilingual_v2"

class NarrationManager:
    """
    Manages the generation of narration audio for educational videos.
    """
    
    def __init__(self):
        self.client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
        
    async def list_available_voices(self) -> List[Dict[str, Any]]:
        """
        Get a list of available voices from ElevenLabs.
        
        Returns:
            List of voice information dictionaries
        """
        try:
            response = self.client.voices.search()
            return [
                {
                    "voice_id": voice.voice_id,
                    "name": voice.name,
                    "description": voice.description,
                    "preview_url": voice.preview_url,
                    "category": voice.category
                }
                for voice in response.voices
            ]
        except Exception as e:
            logger.error(f"Error listing voices: {str(e)}")
            return []
    
    async def generate_narration(
        self, 
        script: str, 
        output_path: str,
        voice_id: str = DEFAULT_VOICE_ID,
        model_id: str = DEFAULT_MODEL_ID,
        stability: float = 0.5,
        clarity: float = 0.75,
        style: float = 0.0,
        max_retries: int = 3,
        retry_delay: float = 2.0
    ) -> Optional[str]:
        """
        Generate narration audio from a script.
        
        Args:
            script: The text to convert to speech
            output_path: Path to save the audio file
            voice_id: ID of the voice to use
            model_id: ID of the model to use
            stability: Voice stability (0.0 to 1.0)
            clarity: Voice clarity/similarity (0.0 to 1.0)
            style: Speaking style (0.0 to 1.0)
            max_retries: Maximum number of retry attempts
            retry_delay: Delay between retries in seconds
            
        Returns:
            Path to the generated audio file or None if failed
        """
        try:
            logger.info(f"Generating narration for script: {script[:100]}...")
            
            # Ensure the output directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Initialize variables for retry loop
            attempts = 0
            last_exception = None
            
            while attempts < max_retries:
                try:
                    logger.info(f"API call attempt {attempts + 1}/{max_retries}")
                    
                    # Generate audio using ElevenLabs API
                    audio = self.client.text_to_speech.convert(
                        text=script,
                        voice_id=voice_id,
                        model_id=model_id,
                        voice_settings={
                            "stability": stability,
                            "similarity_boost": clarity,
                            "style": style,
                        }
                    )
                    
                    # Save the audio to the specified path
                    with open(output_path, "wb") as f:
                        f.write(audio)
                    
                    logger.info(f"Narration audio saved to {output_path}")
                    return output_path
                    
                except Exception as e:
                    last_exception = e
                    logger.warning(f"API call failed with error: {str(e)} (attempt {attempts + 1}/{max_retries})")
                
                # Increment attempt counter and wait before retrying
                attempts += 1
                if attempts < max_retries:
                    logger.info(f"Waiting {retry_delay} seconds before retry...")
                    await asyncio.sleep(retry_delay)
                    # Increase retry delay for subsequent attempts (exponential backoff)
                    retry_delay *= 1.5
            
            # If we've exhausted all retries, raise the last exception
            logger.error(f"All {max_retries} API call attempts failed")
            raise last_exception or ValueError("API call failed after multiple attempts")
            
        except Exception as e:
            logger.error(f"Error generating narration: {str(e)}")
            logger.error(traceback.format_exc())
            return None

    async def extract_narration_from_manim(self, manim_code: str) -> List[Dict[str, Any]]:
        """
        Extract narration text and timing from Manim code.
        
        Args:
            manim_code: The Manim Python code
            
        Returns:
            List of dictionaries containing text and timing information
        """
        try:
            # Extract all Text, Tex, and MathTex objects with their content
            narration_segments = []
            
            # Look for Text objects
            text_matches = self._extract_text_objects(manim_code)
            narration_segments.extend(text_matches)
            
            # Process the segments to create a coherent script
            processed_segments = self._process_narration_segments(narration_segments)
            
            return processed_segments
            
        except Exception as e:
            logger.error(f"Error extracting narration from Manim code: {str(e)}")
            logger.error(traceback.format_exc())
            return []
    
    def _extract_text_objects(self, manim_code: str) -> List[Dict[str, Any]]:
        """
        Extract Text objects from Manim code.
        
        Args:
            manim_code: The Manim Python code
            
        Returns:
            List of dictionaries with text content and metadata
        """
        import re
        
        segments = []
        
        # Pattern for Text objects
        text_pattern = r'Text\(\s*[\'"]([^\'"]*)[\'"]'
        text_matches = re.finditer(text_pattern, manim_code)
        
        for match in text_matches:
            text_content = match.group(1)
            if text_content and len(text_content) > 1:  # Skip empty or single-character texts
                segments.append({
                    "type": "text",
                    "content": text_content,
                    "position": match.start(),
                    "raw_text": text_content
                })
        
        # Pattern for Tex objects (non-math)
        tex_pattern = r'Tex\(\s*[\'"]([^\'"]*)[\'"]'
        tex_matches = re.finditer(tex_pattern, manim_code)
        
        for match in tex_matches:
            tex_content = match.group(1)
            if tex_content and len(tex_content) > 1:
                # Clean up LaTeX commands for narration
                clean_text = self._clean_tex_for_narration(tex_content)
                if clean_text:
                    segments.append({
                        "type": "tex",
                        "content": clean_text,
                        "position": match.start(),
                        "raw_text": tex_content
                    })
        
        # Sort segments by their position in the code
        segments.sort(key=lambda x: x["position"])
        
        return segments
    
    def _clean_tex_for_narration(self, tex_content: str) -> str:
        """
        Clean LaTeX commands for narration.
        
        Args:
            tex_content: The LaTeX content
            
        Returns:
            Cleaned text suitable for narration
        """
        import re
        
        # Remove common LaTeX commands
        cleaned = re.sub(r'\\[a-zA-Z]+', ' ', tex_content)
        
        # Remove LaTeX special characters
        cleaned = re.sub(r'[\\{}$&^_]', ' ', cleaned)
        
        # Replace multiple spaces with a single space
        cleaned = re.sub(r'\s+', ' ', cleaned)
        
        return cleaned.strip()
    
    def _process_narration_segments(self, segments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Process narration segments to create a coherent script.
        
        Args:
            segments: List of extracted text segments
            
        Returns:
            Processed segments with timing estimates
        """
        processed = []
        current_time = 0
        
        for i, segment in enumerate(segments):
            # Skip very short segments or those that are likely not meant for narration
            if len(segment["content"]) < 3:
                continue
                
            # Estimate duration based on word count (average speaking rate: ~150 words per minute)
            word_count = len(segment["content"].split())
            estimated_duration = max(1.0, word_count * 0.4)  # At least 1 second per segment
            
            processed.append({
                "text": segment["content"],
                "start_time": current_time,
                "duration": estimated_duration,
                "type": segment["type"]
            })
            
            # Update the current time for the next segment
            # Add a small gap between segments
            current_time += estimated_duration + 0.5
        
        return processed
    
    async def generate_full_narration(
        self, 
        manim_code: str, 
        output_dir: str,
        voice_id: str = DEFAULT_VOICE_ID,
        model_id: str = DEFAULT_MODEL_ID
    ) -> Dict[str, Any]:
        """
        Generate full narration audio for a Manim animation.
        
        Args:
            manim_code: The Manim Python code
            output_dir: Directory to save the audio files
            voice_id: ID of the voice to use
            model_id: ID of the model to use
            
        Returns:
            Dictionary with narration information
        """
        try:
            # Extract narration segments from the Manim code
            segments = await self.extract_narration_from_manim(manim_code)
            
            if not segments:
                logger.warning("No narration segments found in the Manim code")
                return {"success": False, "error": "No narration segments found"}
            
            # Ensure the output directory exists
            os.makedirs(output_dir, exist_ok=True)
            
            # Combine all segments into a single script
            full_script = " ".join([segment["text"] for segment in segments])
            
            # Generate the full narration audio
            output_path = os.path.join(output_dir, "narration.mp3")
            result = await self.generate_narration(
                script=full_script,
                output_path=output_path,
                voice_id=voice_id,
                model_id=model_id
            )
            
            if not result:
                return {"success": False, "error": "Failed to generate narration audio"}
            
            return {
                "success": True,
                "audio_path": output_path,
                "segments": segments,
                "duration": sum(segment["duration"] for segment in segments)
            }
            
        except Exception as e:
            logger.error(f"Error generating full narration: {str(e)}")
            logger.error(traceback.format_exc())
            return {"success": False, "error": str(e)}