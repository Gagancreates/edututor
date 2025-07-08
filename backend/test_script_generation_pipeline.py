"""
Test script for the enhanced audio-video synchronization pipeline.
"""
import os
import asyncio
import logging
import json
import traceback
from pathlib import Path

from app.services.gemini import generate_manim_code
from app.services.script_generation import generate_script_from_manim_code
from app.services.manim import execute_manim_code_without_audio
from app.services.tts import generate_audio_for_script
from app.services.media_processing import merge_audio_segments_with_video
from app.services.text_extraction import extract_narration_from_manim

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
        try:
            manim_code = await generate_manim_code(prompt, topic, max_retries=2, timeout=180.0)
        except Exception as e:
            logger.error(f"Failed to generate Manim code: {str(e)}")
            return False
        
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
        script_task = asyncio.create_task(
            generate_script_from_manim_code(
                video_id=video_id,
                manim_code=manim_code,
                prompt=prompt,
                topic=topic,
                max_retries=3,
                retry_delay=10.0,
                timeout=360.0  # 6 minutes timeout
            )
        )
        
        # Wait for both tasks to complete
        results = await asyncio.gather(video_task, script_task, return_exceptions=True)
        video_path, script = results
        
        # Handle exceptions if any
        if isinstance(video_path, Exception):
            logger.error(f"Error executing Manim code: {str(video_path)}")
            logger.error(traceback.format_exc())
            return False
            
        if isinstance(script, Exception):
            logger.error(f"Error generating script: {str(script)}")
            logger.info("Using fallback script extraction...")
            # Use the fallback script extraction
            script = extract_narration_from_manim(manim_code)
            logger.info(f"Extracted {len(script)} script segments using fallback method")
        
        # Save the script
        script_path = output_dir / "script.json"
        with open(script_path, "w") as f:
            json.dump(script, f, indent=2)
        logger.info(f"Saved script to {script_path}")
        
        # Step 3: Generate audio for the script
        logger.info("Generating audio...")
        try:
            audio_manifest = await generate_audio_for_script(script, video_id)
            
            # Save the manifest
            manifest_path = output_dir / "manifest.json"
            with open(manifest_path, "w") as f:
                json.dump(audio_manifest, f, indent=2)
            logger.info(f"Saved audio manifest to {manifest_path}")
        except Exception as e:
            logger.error(f"Error generating audio: {str(e)}")
            logger.error(traceback.format_exc())
            return False
        
        # Step 4: Merge audio and video
        logger.info("Merging audio and video...")
        try:
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
            logger.error(f"Error merging audio and video: {str(e)}")
            logger.error(traceback.format_exc())
            return False
            
    except Exception as e:
        logger.error(f"Test failed with error: {str(e)}")
        logger.error(traceback.format_exc())
        return False

if __name__ == "__main__":
    result = asyncio.run(test_script_generation_pipeline())
    if result:
        print("✅ Test completed successfully!")
    else:
        print("❌ Test failed!") 