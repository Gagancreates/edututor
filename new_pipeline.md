# Enhanced Audio-Video Synchronization Pipeline with Two-Step LLM Approach

## Overview

This document outlines an improved implementation plan for audio-video synchronization in EduTutor using a two-step LLM approach:

1. **First API Call**: Generate clean, professional Manim code based on the user's prompt (existing implementation)
2. **Second API Call**: Generate a precisely synchronized script using the LLM based on the generated Manim code
3. **Parallel Processing**: Execute Manim code while waiting for script generation
4. **Audio Generation**: Create audio segments based on the generated script
5. **Media Merging**: Merge audio with video for perfectly synchronized narration

This approach ensures tight synchronization between visual elements and narration, eliminating the need for script extraction from code comments.

## Pipeline Architecture

```
┌──────────────┐    ┌──────────────┐    ┌────────────────┐    
│ User Prompt  │───▶│  LLM Call 1  │───▶│  Manim Code    │───┐    
└──────────────┘    │  Generation  │    │  Generation    │   │    
                    └──────────────┘    └────────────────┘   │    
                                                             │    
                                                             ▼    
┌──────────────┐    ┌──────────────┐    ┌────────────────┐  ┌─────────────┐
│ Final Video  │◀───│  Media       │◀───│  Audio         │  │ Video       │
│ with Audio   │    │  Merging     │    │  Generation    │  │ Generation  │
└──────────────┘    └──────────────┘    └────────────────┘  └─────────────┘
                                                ▲                 │
                                                │                 │
                                        ┌───────────────┐         │
                                        │ LLM Call 2    │◀────────┘
                                        │ Script Gen    │
                                        └───────────────┘
```

## Implementation Steps

### 1. Create Script Generation Service

Create a new service module `script_generation.py` to handle the second LLM call for script generation:

```python
# app/services/script_generation.py
import os
import logging
import json
import asyncio
import google.generativeai as genai
from typing import List, Dict, Any, Optional

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def generate_script_from_manim_code(
    video_id: str,
    manim_code: str,
    prompt: str,
    topic: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Generate a synchronized script for a Manim video using Gemini.
    
    Args:
        video_id: The ID of the video
        manim_code: The Manim code for which to generate a script
        prompt: The original prompt used to generate the Manim code
        topic: The educational topic (optional)
        
    Returns:
        List of script segments with text and timing information
    """
    try:
        logger.info(f"Generating script for video ID: {video_id}")
        
        # Read the prompt template
        with open("docs/prompt2.md", "r") as f:
            prompt_template = f.read()
        
        # Replace placeholder with actual Manim code
        script_prompt = prompt_template.replace("[MANIM_CODE_HERE]", manim_code)
        
        # Add context about the original prompt and topic
        script_prompt = script_prompt.replace(
            "GENERATE SYNCHRONIZED SCRIPT FROM MANIM CODE", 
            f"GENERATE SYNCHRONIZED SCRIPT FROM MANIM CODE\nORIGINAL PROMPT: {prompt}\nTOPIC: {topic or 'Educational content'}"
        )
        
        # Configure Gemini API
        GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not set in environment variables")
            
        genai.configure(api_key=GEMINI_API_KEY)
        
        # Use a more capable model for script generation
        model = genai.GenerativeModel('gemini-1.5-pro')
        
        # Generate the script
        response = await asyncio.to_thread(
            model.generate_content,
            script_prompt,
            generation_config={"temperature": 0.2}  # Lower temperature for more precise output
        )
        
        if not response.text:
            raise ValueError("Empty response from Gemini API")
        
        # Extract the JSON script from the response
        script_text = response.text
        
        # Clean up the response text to extract only the JSON part
        if "```json" in script_text:
            script_text = script_text.split("```json")[1].split("```")[0].strip()
        elif "```" in script_text:
            script_text = script_text.split("```")[1].strip()
        
        # Parse the JSON script
        script = json.loads(script_text)
        
        # Save the script to the video directory
        script_path = os.path.join("videos", video_id, "script.json")
        os.makedirs(os.path.dirname(script_path), exist_ok=True)
        with open(script_path, "w") as f:
            json.dump(script, f, indent=2)
        
        logger.info(f"Successfully generated script for video ID: {video_id}")
        return script
    
    except Exception as e:
        logger.error(f"Error generating script: {str(e)}")
        raise ValueError(f"Failed to generate script: {str(e)}")
```

### 2. Update Video Generation Task

Modify the `generate_video_task` function in `app/routers/generate.py` to implement the two-step approach:

```python
async def generate_video_task(video_id: str, prompt: str, topic: str = None, grade_level: str = None, duration_minutes: float = 3.0):
    try:
        logger.info(f"Starting video generation for ID: {video_id}")
        
        # Create videos directory for this video_id if it doesn't exist
        video_dir = os.path.join("videos", video_id)
        os.makedirs(video_dir, exist_ok=True)
        
        # STEP 1: Generate Manim code using Gemini (first LLM call)
        try:
            manim_code = await generate_manim_code(
                prompt=prompt, 
                topic=topic, 
                grade_level=grade_level, 
                duration_minutes=duration_minutes,
                max_retries=3,
                timeout=180.0
            )
        except Exception as e:
            handle_manim_generation_error(video_id, e)
            return
        
        # Clean the code to remove any Markdown formatting
        if "```" in manim_code:
            logger.warning("Detected Markdown code blocks in the code, cleaning...")
            manim_code = clean_code(manim_code)
        
        # Save the generated code
        code_file = os.path.join(video_dir, f"{video_id}.py")
        with open(code_file, "w") as f:
            f.write(manim_code)
        
        # Start two tasks in parallel:
        # 1. Execute Manim code to generate video
        # 2. Generate script using the second LLM call
        video_task = asyncio.create_task(execute_manim_code_without_audio(video_id, manim_code))
        script_task = asyncio.create_task(
            generate_script_from_manim_code(
                video_id=video_id,
                manim_code=manim_code,
                prompt=prompt,
                topic=topic
            )
        )
        
        # Wait for both tasks to complete
        video_path, script = await asyncio.gather(
            video_task, 
            script_task, 
            return_exceptions=True
        )
        
        # Handle exceptions if any
        if isinstance(video_path, Exception):
            logger.error(f"Error executing Manim code: {str(video_path)}")
            error_file = os.path.join(video_dir, "error.txt")
            with open(error_file, "a") as f:
                f.write(f"\nError executing Manim code: {str(video_path)}")
            return
            
        if isinstance(script, Exception):
            logger.error(f"Error generating script: {str(script)}")
            # Continue with the video generation but use the fallback script extraction
            from app.services.text_extraction import extract_narration_from_manim
            script = extract_narration_from_manim(manim_code)
            logger.info(f"Using fallback script extraction: {len(script)} segments")
        
        # Generate audio for the script
        from app.services.tts import generate_audio_for_script
        audio_manifest = await generate_audio_for_script(script, video_id)
        
        # Merge audio and video
        from app.services.media_processing import merge_audio_segments_with_video
        output_path = await merge_audio_segments_with_video(
            video_path=video_path,
            audio_manifest=audio_manifest,
            output_path=os.path.join(video_dir, f"{video_id}_final.mp4")
        )
        
        # Update metadata
        metadata_file = os.path.join(video_dir, "metadata.json")
        with open(metadata_file, "w") as f:
            metadata = {
                "status": "completed",
                "prompt": prompt,
                "topic": topic,
                "original_video": str(video_path),
                "final_video": str(output_path),
                "script_source": "gemini_generation" if not isinstance(script, Exception) else "fallback_extraction"
            }
            json.dump(metadata, f, indent=2)
        
        logger.info(f"Video generation completed for ID: {video_id}")
    
    except Exception as e:
        logger.error(f"Error generating video {video_id}: {str(e)}")
        logger.error(traceback.format_exc())
        handle_error(video_id, e)
```

### 3. Create a Manim Execution Function without Audio Processing

Add a new function to execute Manim code without audio processing in `app/services/manim.py`:

```python
async def execute_manim_code_without_audio(video_id: str, manim_code: str) -> str:
    """
    Execute Manim code to generate a video without audio processing.
    This is a modified version of execute_manim_code that skips the audio generation step.
    
    Args:
        video_id: Unique identifier for the video
        manim_code: The Manim Python code to execute
        
    Returns:
        Path to the generated video file
    """
    logger.info(f"Starting Manim execution for video ID: {video_id}")
    
    # Check for common errors before execution
    has_errors, error_message = check_for_common_errors(manim_code)
    if has_errors:
        logger.error(f"Code validation failed: {error_message}")
        # Create error files and raise exception
        create_error_files(video_id, f"Code validation failed: {error_message}")
        raise ValueError(f"Code validation failed: {error_message}")
    
    # Output directory for the video
    output_dir = VIDEOS_DIR / video_id
    os.makedirs(output_dir, exist_ok=True)
    
    # Create a temporary directory for this generation
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create the Python file with the Manim code
        script_path = Path(temp_dir) / f"{video_id}.py"
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(manim_code)
        
        try:
            # Execute Manim code and process the results
            # Note: This is similar to the original execute_manim_code but without audio processing
            # Implementation details would be similar to the execute_manim_code function
            # ...
            
            # Find the generated video file
            video_path = find_and_copy_video(temp_dir, output_dir, video_id)
            
            return video_path
            
        except Exception as e:
            logger.error(f"Error executing Manim code: {str(e)}")
            create_error_files(video_id, f"Error executing Manim code: {str(e)}")
            raise
```

### 4. Create Helper Functions

Add the following helper functions to simplify the code:

```python
def handle_manim_generation_error(video_id: str, error: Exception):
    """Handle errors during Manim code generation"""
    logger.error(f"Error generating Manim code: {str(error)}")
    
    # Save detailed error information
    error_file = os.path.join("videos", video_id, "error.txt")
    with open(error_file, "w") as f:
        error_message = f"Failed to generate Manim code: {str(error)}\n\n"
        error_message += "This might be due to:\n"
        error_message += "- The prompt being too complex or broad\n"
        error_message += "- The Gemini API experiencing high traffic\n\n"
        error_message += "Please try:\n"
        error_message += "- Using a more specific and focused prompt\n"
        error_message += "- Breaking down complex topics into smaller parts\n"
        error_message += "- Trying again in a few minutes\n\n"
        error_message += traceback.format_exc()
        f.write(error_message)
    
    # Save metadata for frontend to display
    metadata_file = os.path.join("videos", video_id, "metadata.json")
    with open(metadata_file, "w") as f:
        metadata = {
            "status": "error",
            "error_type": "generation_failed",
            "prompt": prompt,
            "topic": topic,
            "message": f"Failed to generate code: {str(error)}"
        }
        json.dump(metadata, f)
    
    logger.error(f"Generation failed for video {video_id}. Error saved to {error_file}")

def create_error_files(video_id: str, error_message: str):
    """Create error files in the video directory"""
    output_dir = Path("videos") / video_id
    os.makedirs(output_dir, exist_ok=True)
    
    error_path = output_dir / "error.txt"
    try:
        with open(error_path, "w", encoding="utf-8") as f:
            f.write(f"{error_message}\n\n")
            f.write(traceback.format_exc())
    except UnicodeEncodeError:
        with open(error_path, "w", encoding="utf-8", errors="replace") as f:
            f.write(f"{error_message}\n\n")
            f.write("[Some characters were replaced due to encoding issues]")
```

## Testing Framework

### 1. Create a Test Script for the New Pipeline

Create a test script `test_script_generation_pipeline.py` to verify the new implementation:

```python
"""
Test script for the enhanced audio-video synchronization pipeline.
"""
import os
import asyncio
import logging
import json
from pathlib import Path

from app.services.gemini import generate_manim_code
from app.services.script_generation import generate_script_from_manim_code
from app.services.manim import execute_manim_code_without_audio
from app.services.tts import generate_audio_for_script
from app.services.media_processing import merge_audio_segments_with_video

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_script_generation_pipeline():
    """
    Test the enhanced audio-video synchronization pipeline.
    """
    try:
        # Test parameters
        video_id = "test_script_gen"
        prompt = "Explain linked lists with a clear visualization"
        topic = "Data Structures"
        output_dir = Path(f"./temp/{video_id}")
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Step 1: Generate Manim code
        logger.info("Generating Manim code...")
        manim_code = await generate_manim_code(prompt, topic)
        
        # Save the generated code
        code_path = output_dir / "code.py"
        with open(code_path, "w") as f:
            f.write(manim_code)
        logger.info(f"Saved Manim code to {code_path}")
        
        # Step 2: Start two parallel tasks
        # - Generate video from Manim code
        # - Generate script from Manim code
        logger.info("Starting parallel tasks...")
        video_task = asyncio.create_task(execute_manim_code_without_audio(video_id, manim_code))
        script_task = asyncio.create_task(generate_script_from_manim_code(video_id, manim_code, prompt, topic))
        
        # Wait for both tasks to complete
        video_path, script = await asyncio.gather(video_task, script_task)
        
        # Save the script
        script_path = output_dir / "script.json"
        with open(script_path, "w") as f:
            json.dump(script, f, indent=2)
        logger.info(f"Saved script to {script_path}")
        
        # Step 3: Generate audio for the script
        logger.info("Generating audio...")
        audio_manifest = await generate_audio_for_script(script, video_id)
        
        # Save the manifest
        manifest_path = output_dir / "manifest.json"
        with open(manifest_path, "w") as f:
            json.dump(audio_manifest, f, indent=2)
        logger.info(f"Saved audio manifest to {manifest_path}")
        
        # Step 4: Merge audio and video
        logger.info("Merging audio and video...")
        output_path = await merge_audio_segments_with_video(
            video_path=video_path,
            audio_manifest=audio_manifest,
            output_path=output_dir / "final_video.mp4"
        )
        
        if output_path and os.path.exists(output_path):
            logger.info(f"Successfully created final video: {output_path}")
            return True
        else:
            logger.error("Failed to create final video")
            return False
            
    except Exception as e:
        logger.error(f"Test failed with error: {str(e)}")
        return False

if __name__ == "__main__":
    asyncio.run(test_script_generation_pipeline())
```

## Implementation Timeline

### Phase 1: Core Implementation (1-2 days)

1. Create the `script_generation.py` service
2. Update the `generate_video_task` function
3. Create the `execute_manim_code_without_audio` function

### Phase 2: Testing and Refinement (1-2 days)

1. Create the test script
2. Test with various educational topics and prompts
3. Compare results with the original implementation
4. Fine-tune the script generation prompt

### Phase 3: Production Deployment (1 day)

1. Update API documentation
2. Deploy to production
3. Monitor performance and results

## Audio-Video Merging Process

The merging of audio segments with the video is a critical part of the pipeline that ensures proper synchronization. This section details how the audio-video merging will work in the enhanced pipeline.

### 1. Advanced FFmpeg Integration

The existing `merge_audio_segments_with_video` function in `media_processing.py` will continue to be used, but with special consideration for the precise timing information provided by the LLM-generated script:

```python
async def merge_audio_segments_with_video(
    video_path: Union[str, Path],
    audio_manifest: Dict[str, Any],
    output_path: Optional[Union[str, Path]] = None,
    overwrite: bool = True
) -> Optional[Path]:
    """
    Merge audio segments with a video using FFmpeg.
    
    This function takes timing information from the audio_manifest and places
    each audio segment at the exact timestamp specified in the manifest.
    
    Args:
        video_path: Path to the video file
        audio_manifest: Audio manifest with paths to audio segments and timing information
        output_path: Path to save the output file (if None, a path will be generated)
        overwrite: Whether to overwrite the output file if it exists
        
    Returns:
        Path to the merged video file or None if merging failed
    """
    # Implementation details...
```

### 2. Precise Timing Control

The audio-video merging process will specifically leverage the precise timing information in the LLM-generated script:

1. **Create a Silent Base Track**: Generate a silent audio track that matches the duration of the video
2. **Add Each Audio Segment with Exact Timing**: Place each segment at its specific timestamp using FFmpeg's `adelay` filter
3. **Mix All Segments**: Combine all segments into a single audio track using the `amix` filter
4. **Merge with Video**: Combine the mixed audio track with the video using FFmpeg's mapping capabilities

The core FFmpeg filter graph will look like:

```
[0]adelay=start_time_ms|start_time_ms[a1];
[1]adelay=start_time_ms|start_time_ms[a2];
...
[0][a1][a2]...[aN]amix=inputs=N+1:duration=longest[aout]
```

### 3. Handling Pauses and Pacing

The LLM-generated script will include strategic pauses that enhance comprehension:

1. **Explicit Pause Segments**: Script segments with type "pause" will be represented as silence in the final audio
2. **Natural Pacing**: The timing of each segment accounts for natural speaking pace and pauses
3. **SSML Tags**: Speech Synthesis Markup Language tags in the script control pacing and emphasis

### 4. Implementation Details

The implementation will use the existing `merge_audio_segments_with_video` function with the following enhancements:

1. **Enhanced Timing Extraction**: Extract exact start times from the script segments
2. **Complex Filter Graph**: Build a more sophisticated FFmpeg filter graph for precise timing
3. **Quality Control**: Ensure high audio quality with appropriate bitrate and audio codec settings
4. **Error Handling**: Robust error handling and fallback mechanisms

Example of the enhanced FFmpeg command:

```python
cmd = [
    "ffmpeg", "-y",
    "-i", str(video_path),  # Input video
    *input_audio_files,     # Input audio segments
    "-filter_complex", filter_complex,  # Complex filter graph for precise timing
    "-map", "0:v",          # Map video from first input
    "-map", "[aout]",       # Map audio from filter output
    "-c:v", "copy",         # Copy video codec (no re-encoding)
    "-c:a", "aac",          # Use AAC audio codec
    "-b:a", "192k",         # Set audio bitrate
    "-shortest",            # End when shortest input ends
    str(output_path)        # Output file
]
```

This approach ensures that each narration segment is placed exactly where it should be in relation to the visual elements in the video, creating a professional and synchronized educational experience.

## Conclusion

This enhanced audio-video synchronization pipeline offers significant advantages:

1. **Improved Synchronization**: The LLM-generated script precisely aligns with the video content
2. **Parallel Processing**: Video generation and script generation run simultaneously for efficiency
3. **Better Educational Experience**: Professional narration with strategic pauses enhances learning
4. **Fallback Mechanism**: Original script extraction serves as a backup if LLM generation fails
5. **Seamless Integration**: Works with the existing frontend and API without changes to client code
6. **Professional Audio Placement**: Precise FFmpeg commands ensure each narration segment is placed exactly at the right timestamp

By implementing this improved pipeline, EduTutor will deliver higher-quality educational videos with perfectly synchronized narration, creating a more engaging and effective learning experience. 