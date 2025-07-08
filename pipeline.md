# Enhanced Audio-Video Synchronization Pipeline

## Overview

This document outlines the implementation plan for enhancing audio-video synchronization in EduTutor using a two-step LLM approach:

1. **First LLM Call**: Generate clean, professional Manim code based on the user's prompt
2. **Second LLM Call**: Generate a synchronized narration script that aligns precisely with the video content

This approach ensures tight synchronization between visual elements and narration, creating a professional educational experience with properly timed pauses and transitions.

## Pipeline Architecture

```
┌──────────────┐    ┌──────────────┐    ┌────────────────┐    ┌───────────────┐
│ User Prompt  │───▶│  LLM Call 1  │───▶│  Manim Code    │───▶│ Video         │
└──────────────┘    │  Generation  │    │  Execution     │    │ Generation    │
                    └──────────────┘    └────────────────┘    └───────┬───────┘
                                                                      │
                                                                      ▼
┌──────────────┐    ┌──────────────┐    ┌────────────────┐    ┌───────────────┐
│ Final Video  │◀───│  Media       │◀───│  Audio         │◀───│ LLM Call 2    │
│ with Audio   │    │  Merging     │    │  Generation    │    │ Script Gen    │
└──────────────┘    └──────────────┘    └────────────────┘    └───────────────┘
```

## Detailed Implementation Steps

### 1. Enhanced Video Generation Service

#### 1.1 Update `generate_video_task` Function

```python
async def generate_video_task(video_id, prompt, topic=None, grade_level=None, duration_minutes=3.0):
    try:
        # Create directory structure
        video_dir = os.path.join("videos", video_id)
        os.makedirs(video_dir, exist_ok=True)
        
        # STEP 1: Generate Manim code using first LLM call
        manim_code = await generate_manim_code(
            prompt=prompt, 
            topic=topic, 
            grade_level=grade_level, 
            duration_minutes=duration_minutes,
            max_retries=3,
            timeout=180.0
        )
        
        # Clean code and save
        manim_code = clean_code(manim_code)
        code_file = os.path.join(video_dir, f"{video_id}.py")
        with open(code_file, "w") as f:
            f.write(manim_code)
        
        # Execute Manim code to generate video
        video_path = await execute_manim_code(video_id, manim_code)
        
        # STEP 2: Generate synchronized script using second LLM call
        script = await generate_synchronized_script(
            video_id=video_id,
            manim_code=manim_code,
            video_path=video_path,
            prompt=prompt,
            topic=topic
        )
        
        # Generate audio from script
        audio_manifest = await generate_audio_for_script(script, video_id)
        
        # Merge audio and video
        output_path = await merge_audio_segments_with_video(
            video_path=video_path,
            audio_manifest=audio_manifest,
            output_path=os.path.join(video_dir, f"{video_id}_final.mp4")
        )
        
        # Update metadata
        update_video_metadata(video_id, {
            "status": "completed",
            "original_video": str(video_path),
            "final_video": str(output_path),
            "script": script
        })
        
    except Exception as e:
        handle_error(video_id, e)
```

### 2. Synchronized Script Generation Service

#### 2.1 Create `script_generation.py` Service

```python
"""
Script generation service for creating synchronized narration scripts.
"""
import os
import logging
import asyncio
import json
from typing import List, Dict, Any, Optional, Union
from pathlib import Path
import google.generativeai as genai

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def generate_synchronized_script(
    video_id: str,
    manim_code: str,
    video_path: Union[str, Path],
    prompt: str,
    topic: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Generate a synchronized narration script for a Manim video.
    
    This function uses a second LLM call to create a script that aligns
    with the visual elements in the video, including proper timing information.
    
    Args:
        video_id: The ID of the video
        manim_code: The Manim code used to generate the video
        video_path: Path to the generated video
        prompt: The original prompt used to generate the video
        topic: The educational topic (optional)
        
    Returns:
        List of script segments with text and precise timing information
    """
    try:
        logger.info(f"Generating synchronized script for video {video_id}")
        
        # Extract timing information from Manim code
        timing_info = extract_timing_information(manim_code)
        
        # Create the prompt for the second LLM call
        script_prompt = create_script_generation_prompt(
            manim_code=manim_code,
            timing_info=timing_info,
            original_prompt=prompt,
            topic=topic
        )
        
        # Generate script using Gemini
        script = await generate_script_with_gemini(script_prompt)
        
        # Enhance script with strategic pauses
        enhanced_script = insert_strategic_pauses(script)
        
        # Add SSML tags for better speech synthesis
        final_script = add_ssml_tags_to_script(enhanced_script)
        
        # Save script for future reference
        script_file = os.path.join("videos", video_id, "script.json")
        os.makedirs(os.path.dirname(script_file), exist_ok=True)
        with open(script_file, "w") as f:
            json.dump(final_script, f, indent=2)
        
        logger.info(f"Successfully generated synchronized script for video {video_id}")
        return final_script
    
    except Exception as e:
        logger.error(f"Error generating synchronized script: {str(e)}")
        raise ValueError(f"Failed to generate synchronized script: {str(e)}")

def extract_timing_information(manim_code: str) -> Dict[str, Any]:
    """
    Extract timing information from Manim code.
    
    This function analyzes the Manim code to identify:
    1. Scene structure and timing
    2. Animation sequences with durations
    3. Wait times
    4. Text elements and their appearance timings
    
    Args:
        manim_code: The Manim code to analyze
        
    Returns:
        Dictionary with timing information
    """
    import re
    
    # Initialize timing dictionary
    timing_info = {
        "total_duration": 0.0,
        "scenes": [],
        "animations": [],
        "wait_times": [],
        "text_elements": []
    }
    
    # Extract scene classes
    scene_pattern = r"class\s+(\w+)\(.*\):\s*(?:[^\{])*(?:def\s+construct\s*\(\s*self\s*\):\s*((?:.*?\n)+?)(?:def|\Z))"
    scene_matches = re.finditer(scene_pattern, manim_code, re.DOTALL)
    
    current_time = 0.0
    
    for match in scene_matches:
        scene_name = match.group(1)
        construct_content = match.group(2)
        scene_start_time = current_time
        
        # Extract wait times
        wait_pattern = r"self\.wait\s*\(\s*(\d+\.?\d*)\s*\)"
        wait_matches = re.finditer(wait_pattern, construct_content)
        
        for wait_match in wait_matches:
            wait_time = float(wait_match.group(1))
            timing_info["wait_times"].append({
                "time": current_time,
                "duration": wait_time
            })
            current_time += wait_time
        
        # Extract animations and their durations
        play_pattern = r"self\.play\s*\((.*?)(?:,\s*run_time\s*=\s*(\d+\.?\d*))?(?:,|\))"
        play_matches = re.finditer(play_pattern, construct_content, re.DOTALL)
        
        for play_match in play_matches:
            animation = play_match.group(1)
            duration = float(play_match.group(2)) if play_match.group(2) else 1.0
            
            timing_info["animations"].append({
                "animation": animation.strip(),
                "time": current_time,
                "duration": duration
            })
            current_time += duration
        
        # Extract text elements
        text_pattern = r"(?:Text|Tex|MathTex|Title)\s*\(\s*(?:r?[\"'])([^\"']+)(?:[\"'])"
        text_matches = re.finditer(text_pattern, construct_content)
        
        for text_match in text_matches:
            text = text_match.group(1)
            # Find the closest animation after this text declaration
            text_pos = text_match.start()
            closest_anim_time = current_time
            
            for anim in timing_info["animations"]:
                anim_pos = construct_content.find(anim["animation"])
                if anim_pos > text_pos:
                    closest_anim_time = anim["time"]
                    break
            
            timing_info["text_elements"].append({
                "text": text,
                "time": closest_anim_time,
                "type": "text_object"
            })
        
        # Add scene information
        timing_info["scenes"].append({
            "name": scene_name,
            "start_time": scene_start_time,
            "end_time": current_time,
            "duration": current_time - scene_start_time
        })
    
    # Update total duration
    timing_info["total_duration"] = current_time
    
    return timing_info

def create_script_generation_prompt(
    manim_code: str, 
    timing_info: Dict[str, Any],
    original_prompt: str,
    topic: Optional[str] = None
) -> str:
    """
    Create a prompt for generating a synchronized script.
    
    Args:
        manim_code: The Manim code for the video
        timing_info: Extracted timing information
        original_prompt: The original prompt used to generate the video
        topic: The educational topic (optional)
        
    Returns:
        Prompt string for the LLM
    """
    # Create a structured representation of the timing information
    text_elements_json = json.dumps(timing_info["text_elements"], indent=2)
    scenes_json = json.dumps(timing_info["scenes"], indent=2)
    wait_times_json = json.dumps(timing_info["wait_times"], indent=2)
    
    # Build the prompt
    prompt = f"""
TASK: Create a precisely synchronized narration script for an educational video

CONTEXT:
- Original topic: {topic or 'Educational content'}
- Original prompt: {original_prompt}
- Total video duration: {timing_info['total_duration']} seconds

TIMING INFORMATION:
- Text elements (with timing):
{text_elements_json}

- Scene structure:
{scenes_json}

- Wait times (pauses):
{wait_times_json}

MANIM CODE:
```python
{manim_code}
```

REQUIREMENTS:
1. Generate a narration script with EXACT timing that matches the video content
2. Each script segment must follow this JSON format:
   {{
     "text": "What are Linked Lists?",
     "timing": {{
       "start": 3.0,
       "duration": 1.875
     }},
     "type": "text_object"
   }}
3. Ensure "start" times align perfectly with when visual elements appear in the video
4. Calculate appropriate "duration" values for each segment based on text length
5. Add pauses between conceptual segments using "pause" type
6. Ensure total narration fits within the video duration ({timing_info['total_duration']} seconds)
7. Make narration educational, clear, and matched to the visuals
8. Return ONLY a valid JSON array of script segments

OUTPUT FORMAT:
Return ONLY a JSON array of script segments with precise timing information.
"""
    
    return prompt

async def generate_script_with_gemini(prompt: str) -> List[Dict[str, Any]]:
    """
    Generate a synchronized script using Gemini API.
    
    Args:
        prompt: The script generation prompt
        
    Returns:
        List of script segments with timing information
    """
    try:
        # Configure the Gemini API
        GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-pro')
        
        # Generate the script
        response = await asyncio.to_thread(model.generate_content, prompt)
        
        if not response.text:
            raise ValueError("Empty response from Gemini API")
        
        # Parse the JSON response
        script_text = response.text
        
        # Clean up the response text to extract only the JSON part
        if "```json" in script_text:
            script_text = script_text.split("```json")[1].split("```")[0].strip()
        elif "```" in script_text:
            script_text = script_text.split("```")[1].strip()
        
        script = json.loads(script_text)
        
        # Validate script format
        if not isinstance(script, list):
            raise ValueError("Script must be a list of segments")
        
        for segment in script:
            if not isinstance(segment, dict):
                raise ValueError("Each script segment must be a dictionary")
            if "text" not in segment:
                raise ValueError("Each script segment must have a 'text' field")
            if "timing" not in segment:
                raise ValueError("Each script segment must have a 'timing' field")
            if "start" not in segment["timing"]:
                raise ValueError("Each script segment timing must have a 'start' field")
            if "duration" not in segment["timing"]:
                raise ValueError("Each script segment timing must have a 'duration' field")
        
        return script
    
    except Exception as e:
        logger.error(f"Error generating script with Gemini: {str(e)}")
        raise ValueError(f"Failed to generate script: {str(e)}")

def insert_strategic_pauses(script: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Insert strategic pauses between script segments.
    
    Args:
        script: List of script segments
        
    Returns:
        Enhanced script with strategic pauses
    """
    enhanced_script = []
    
    for i, segment in enumerate(script):
        # Add the segment itself
        enhanced_script.append(segment)
        
        # Add pause after the segment if it's not the last one
        if i < len(script) - 1:
            next_segment = script[i + 1]
            
            # Calculate time gap to next segment
            segment_end = segment["timing"]["start"] + segment["timing"]["duration"]
            next_segment_start = next_segment["timing"]["start"]
            time_gap = next_segment_start - segment_end
            
            # If there's a significant gap, add a pause
            if time_gap > 1.0:
                pause_duration = min(time_gap, 3.0)  # Cap at 3 seconds
                enhanced_script.append({
                    "text": f"<break time='{pause_duration}s'/>",
                    "timing": {
                        "start": segment_end,
                        "duration": pause_duration
                    },
                    "type": "pause"
                })
    
    return enhanced_script

def add_ssml_tags_to_script(script: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Add SSML tags to script segments for better speech synthesis.
    
    Args:
        script: List of script segments
        
    Returns:
        Enhanced script with SSML tags
    """
    for segment in script:
        # Skip if already a pause or already has SSML tags
        if segment["type"] == "pause" or "<break" in segment["text"] or "<prosody" in segment["text"]:
            continue
        
        # Determine appropriate speech rate based on content length and segment duration
        text_length = len(segment["text"].split())
        segment_duration = segment["timing"]["duration"]
        
        if text_length / segment_duration > 3.0:  # More than 3 words per second
            rate = "slow"
        elif text_length / segment_duration < 1.5:  # Less than 1.5 words per second
            rate = "medium"
        else:
            rate = "medium"
        
        # Add prosody tags for rate control
        segment["text"] = f"<prosody rate='{rate}'>{segment['text']}</prosody>"
    
    return script
```

### 3. Audio Generation and Media Merging

#### 3.1 Update TTS Service for Script Awareness

Enhance the `tts.py` service to handle the script format from the LLM:

```python
async def generate_audio_for_script(script, video_id, voice_id=None):
    """
    Generate audio for a synchronized script.
    
    Args:
        script: List of script segments with timing information
        video_id: ID of the video
        voice_id: ID of the voice to use (optional)
        
    Returns:
        Audio manifest with paths to generated audio segments
    """
    # Use default voice ID if none provided
    if voice_id is None:
        voice_id = DEFAULT_VOICE_ID
    
    # Create directory for audio files
    audio_dir = os.path.join("audio", video_id)
    os.makedirs(audio_dir, exist_ok=True)
    
    # Generate audio for each segment
    segments = []
    
    for i, segment in enumerate(script):
        # Skip pauses (they will be handled as silence in the final merge)
        if segment["type"] == "pause":
            continue
        
        # Generate audio for this segment
        segment_path = os.path.join(audio_dir, f"segment_{i:03d}.mp3")
        
        # Generate audio using Eleven Labs API
        success = await generate_segment_audio(
            text=segment["text"],
            output_path=segment_path,
            voice_id=voice_id
        )
        
        if success:
            segments.append({
                "index": i,
                "text": segment["text"],
                "timing": segment["timing"],
                "audio_path": segment_path,
                "type": segment["type"]
            })
    
    # Create manifest
    manifest = {
        "video_id": video_id,
        "voice_id": voice_id,
        "segments": segments
    }
    
    # Save manifest
    manifest_path = os.path.join(audio_dir, "manifest.json")
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)
    
    return manifest
```

#### 3.2 Enhanced Media Processing for Precise Sync

Update the media processing service to handle precise timing information:

```python
async def merge_audio_segments_with_timing(
    video_path,
    audio_manifest,
    output_path=None,
    overwrite=True
):
    """
    Merge audio segments with precise timing alignment using a complex FFmpeg filter graph.
    
    Args:
        video_path: Path to the video file
        audio_manifest: Audio manifest with paths to audio segments and timing information
        output_path: Path for the output file (optional)
        overwrite: Whether to overwrite existing files (default: True)
        
    Returns:
        Path to the merged video file
    """
    try:
        # Prepare paths
        video_path = Path(video_path)
        if output_path is None:
            output_path = video_path.parent / f"{video_path.stem}_narrated{video_path.suffix}"
        output_path = Path(output_path)
        
        # Create a temporary directory for processing
        with tempfile.TemporaryDirectory(dir=TEMP_DIR) as temp_dir:
            temp_dir_path = Path(temp_dir)
            
            # Create a silent audio track matching video duration
            video_info = get_video_info(video_path)
            video_duration = float(video_info["duration"])
            
            silent_audio_path = temp_dir_path / "silent.mp3"
            generate_silent_audio(silent_audio_path, video_duration)
            
            # Create a complex filter graph for precise timing
            audio_segments = audio_manifest.get("segments", [])
            
            if not audio_segments:
                logger.error("No audio segments found in manifest")
                return None
            
            # Prepare filter complex parts
            inputs = []
            filter_parts = []
            
            # First input is the silent base track
            inputs.append("-i")
            inputs.append(str(silent_audio_path))
            
            # Add each audio segment with precise timing
            for i, segment in enumerate(audio_segments):
                if "audio_path" not in segment or not Path(segment["audio_path"]).exists():
                    continue
                
                # Add input for this segment
                inputs.append("-i")
                inputs.append(segment["audio_path"])
                
                # Calculate segment timing
                start_time = segment["timing"]["start"]
                
                # Add to filter complex
                filter_parts.append(f"[{i+1}]adelay={int(start_time*1000)}|{int(start_time*1000)}[a{i+1}]")
            
            # Mix all audio segments with the base silent track
            mix_parts = ["[0]"]
            for i in range(len(audio_segments)):
                mix_parts.append(f"[a{i+1}]")
            
            filter_parts.append(f"{' '.join(mix_parts)}amix=inputs={len(mix_parts)}:duration=longest[aout]")
            
            # Build the FFmpeg command
            cmd = [
                "ffmpeg", "-y",
                "-i", str(video_path),
                *inputs,
                "-filter_complex", ";".join(filter_parts),
                "-map", "0:v", "-map", "[aout]",
                "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                str(output_path)
            ]
            
            # Execute the FFmpeg command
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                logger.error(f"FFmpeg error: {stderr.decode()}")
                return None
            
            logger.info(f"Successfully merged audio segments with precise timing to {output_path}")
            return output_path
    
    except Exception as e:
        logger.error(f"Error merging audio segments with timing: {str(e)}")
        return None
```

### 4. Testing Framework

#### 4.1 End-to-End Test Script

Create a comprehensive test script to validate the new pipeline:

```python
"""
End-to-end test for the enhanced audio-video sync pipeline.
"""
import os
import asyncio
import logging
from pathlib import Path

from app.services.gemini import generate_manim_code
from app.services.manim import execute_manim_code
from app.services.script_generation import generate_synchronized_script
from app.services.tts import generate_audio_for_script
from app.services.media_processing import merge_audio_segments_with_timing

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_e2e_pipeline():
    """
    Test the complete end-to-end pipeline.
    """
    try:
        # Test parameters
        video_id = "test_e2e"
        prompt = "Explain linked lists with a clear visualization"
        topic = "Data Structures"
        
        # Step 1: Generate Manim code
        logger.info("Generating Manim code...")
        manim_code = await generate_manim_code(prompt, topic)
        
        # Save the generated code
        os.makedirs(f"./temp/{video_id}", exist_ok=True)
        with open(f"./temp/{video_id}/code.py", "w") as f:
            f.write(manim_code)
        
        # Step 2: Execute Manim code
        logger.info("Executing Manim code...")
        video_path = await execute_manim_code(video_id, manim_code)
        
        # Step 3: Generate synchronized script
        logger.info("Generating synchronized script...")
        script = await generate_synchronized_script(
            video_id=video_id,
            manim_code=manim_code,
            video_path=video_path,
            prompt=prompt,
            topic=topic
        )
        
        # Save the script
        with open(f"./temp/{video_id}/script.json", "w") as f:
            import json
            json.dump(script, f, indent=2)
        
        # Step 4: Generate audio for script
        logger.info("Generating audio...")
        audio_manifest = await generate_audio_for_script(script, video_id)
        
        # Step 5: Merge audio and video with precise timing
        logger.info("Merging audio and video...")
        output_path = await merge_audio_segments_with_timing(
            video_path=video_path,
            audio_manifest=audio_manifest,
            output_path=f"./temp/{video_id}/output.mp4"
        )
        
        if output_path and os.path.exists(output_path):
            logger.info(f"Pipeline test successful! Output: {output_path}")
            return True
        else:
            logger.error("Pipeline test failed: Output not generated")
            return False
            
    except Exception as e:
        logger.error(f"Pipeline test failed with error: {str(e)}")
        return False

if __name__ == "__main__":
    asyncio.run(test_e2e_pipeline())
```

## Implementation Timeline

### Phase 1: Core Services (Days 1-2)

1. Create `script_generation.py` service with:
   - Timing extraction from Manim code
   - Script generation with Gemini
   - SSML enhancement for better speech

2. Update TTS service for script awareness:
   - Support for synchronized segment generation
   - Proper handling of pauses and timing

### Phase 2: Enhanced Media Processing (Days 3-4)

1. Implement precise audio placement with FFmpeg:
   - Complex filter graph for timing control
   - Silence insertion for pauses
   - Audio mixing with proper synchronization

2. Update the media processing service with:
   - New audio merging function with timing control
   - Improved error handling and logging

### Phase 3: Pipeline Integration (Days 5-6)

1. Update `generate_video_task` to implement the two-step process
2. Add script generation to the pipeline
3. Integrate with existing components

### Phase 4: Testing and Refinement (Days 7-8)

1. Create end-to-end test script
2. Perform comprehensive testing with various examples
3. Refine timing and synchronization based on results

## Conclusion

This enhanced audio-video synchronization pipeline will create a professional educational experience with precisely timed narration. The two-step approach allows for:

1. Clean, focused Manim code generation without distraction
2. Specialized script generation that focuses on timing and synchronization
3. Professional narration that aligns perfectly with visual elements
4. Strategic pauses that enhance comprehension

By implementing this pipeline, we'll achieve a significant improvement in the quality of educational videos generated by EduTutor, providing a more engaging and effective learning experience. 