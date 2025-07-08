"""
Test script for the full pipeline from generating Manim code with NARRATION comments
to extracting the narration and creating a synchronized video.
"""
import os
import asyncio
import logging
import json
import traceback
from pathlib import Path

from app.services.gemini import generate_manim_code
from app.services.manim import execute_manim_code_without_audio
from app.services.text_extraction import extract_narration_from_manim
from app.services.tts import generate_audio_for_script
from app.services.media_processing import merge_audio_segments_with_video

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_narration_pipeline():
    """
    Test the full pipeline from generating Manim code with NARRATION comments
    to extracting the narration and creating a synchronized video.
    """
    try:
        # Test parameters
        video_id = "test_narration_pipeline"
        prompt = "Explain the Pythagorean theorem with visual proof"
        topic = "Geometry"
        output_dir = Path(f"./temp/{video_id}")
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        logger.info("=== Step 1: Generate Manim code with NARRATION comments ===")
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
        
        logger.info("=== Step 2: Extract narration from the Manim code ===")
        script = extract_narration_from_manim(manim_code)
        
        # Save the script
        script_path = output_dir / "script.json"
        with open(script_path, "w") as f:
            json.dump(script, f, indent=2)
        logger.info(f"Saved script to {script_path}")
        
        # Print the extracted narration
        logger.info(f"Extracted {len(script)} narration segments:")
        for i, segment in enumerate(script[:3]):  # Show first 3 segments
            logger.info(f"Segment {i+1}: {segment['text'][:50]}... (duration: {segment['timing']['duration']}s)")
        
        logger.info("=== Step 3: Generate video from Manim code ===")
        try:
            video_path = await execute_manim_code_without_audio(video_id, manim_code)
            logger.info(f"Generated video: {video_path}")
        except Exception as e:
            logger.error(f"Failed to generate video: {str(e)}")
            logger.error(traceback.format_exc())
            return False
        
        logger.info("=== Step 4: Generate audio for the script ===")
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
        
        logger.info("=== Step 5: Merge audio and video ===")
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
    print("=== Testing full narration pipeline ===")
    result = asyncio.run(test_narration_pipeline())
    
    if result:
        print("✅ Test completed successfully!")
    else:
        print("❌ Test failed!") 