"""
Test script to verify that the audio narration flow works correctly with the new processing marker.
"""
import os
import sys
import asyncio
import logging
import uuid
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Add the parent directory to the path so we can import from app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the helper functions
from app.utils.helpers import get_video_path, get_video_status, create_audio_processing_marker, remove_audio_processing_marker, is_audio_processing

async def test_audio_processing_marker():
    """Test that the audio processing marker functions work correctly."""
    # Generate a test video ID
    test_video_id = f"test_audio_marker_{uuid.uuid4().hex[:8]}"
    
    try:
        # Create the marker
        create_audio_processing_marker(test_video_id)
        
        # Check if the marker exists
        if is_audio_processing(test_video_id):
            logger.info("✅ PASS: Audio processing marker created successfully")
        else:
            logger.error("❌ FAIL: Audio processing marker was not created")
            return False
        
        # Check the video status
        status = get_video_status(test_video_id)
        
        if status["status"] == "processing" and "audio narration" in status["message"].lower():
            logger.info("✅ PASS: Video status correctly shows audio processing")
        else:
            logger.error(f"❌ FAIL: Video status does not show audio processing: {status}")
            return False
        
        # Create a dummy video file
        video_dir = Path(f"./videos/{test_video_id}")
        video_dir.mkdir(parents=True, exist_ok=True)
        video_path = video_dir / f"{test_video_id}.mp4"
        
        with open(video_path, "wb") as f:
            f.write(b"This is a dummy video file")
        
        # Check that get_video_path returns None while audio is processing
        path = get_video_path(test_video_id)
        
        if path is None:
            logger.info("✅ PASS: get_video_path correctly returns None during audio processing")
        else:
            logger.error(f"❌ FAIL: get_video_path returned a path during audio processing: {path}")
            return False
        
        # Remove the marker
        remove_audio_processing_marker(test_video_id)
        
        # Check if the marker is gone
        if not is_audio_processing(test_video_id):
            logger.info("✅ PASS: Audio processing marker removed successfully")
        else:
            logger.error("❌ FAIL: Audio processing marker was not removed")
            return False
        
        # Check that get_video_path now returns the video path
        path = get_video_path(test_video_id)
        
        if path is not None:
            logger.info("✅ PASS: get_video_path correctly returns the video path after audio processing")
        else:
            logger.error("❌ FAIL: get_video_path returned None after audio processing")
            return False
        
        # Check the video status again
        status = get_video_status(test_video_id)
        
        if status["status"] == "completed":
            logger.info("✅ PASS: Video status correctly shows completed after audio processing")
        else:
            logger.error(f"❌ FAIL: Video status does not show completed after audio processing: {status}")
            return False
        
        return True
    
    finally:
        # Clean up
        video_dir = Path(f"./videos/{test_video_id}")
        if video_dir.exists():
            import shutil
            shutil.rmtree(video_dir)
            logger.info(f"Cleaned up test directory {video_dir}")

async def test_narrated_video_priority():
    """Test that narrated videos are prioritized over original videos."""
    # Generate a test video ID
    test_video_id = f"test_narration_priority_{uuid.uuid4().hex[:8]}"
    
    try:
        # Create the video directory
        video_dir = Path(f"./videos/{test_video_id}")
        video_dir.mkdir(parents=True, exist_ok=True)
        
        # Create a dummy original video file
        original_video_path = video_dir / f"{test_video_id}.mp4"
        with open(original_video_path, "wb") as f:
            f.write(b"This is a dummy original video file")
        
        # Create the audio processing marker
        create_audio_processing_marker(test_video_id)
        
        # Check that get_video_path returns None while audio is processing
        path = get_video_path(test_video_id)
        
        if path is None:
            logger.info("✅ PASS: get_video_path correctly returns None during audio processing")
        else:
            logger.error(f"❌ FAIL: get_video_path returned a path during audio processing: {path}")
            return False
        
        # Create a dummy narrated video file
        narrated_video_path = video_dir / f"{test_video_id}_with_audio.mp4"
        with open(narrated_video_path, "wb") as f:
            f.write(b"This is a dummy narrated video file")
        
        # Remove the audio processing marker
        remove_audio_processing_marker(test_video_id)
        
        # Check that get_video_path returns the narrated video path
        path = get_video_path(test_video_id)
        
        if path is not None and "_with_audio" in path:
            logger.info("✅ PASS: get_video_path correctly returns the narrated video path")
        else:
            logger.error(f"❌ FAIL: get_video_path did not return the narrated video path: {path}")
            return False
        
        return True
    
    finally:
        # Clean up
        video_dir = Path(f"./videos/{test_video_id}")
        if video_dir.exists():
            import shutil
            shutil.rmtree(video_dir)
            logger.info(f"Cleaned up test directory {video_dir}")

async def main():
    """Run the tests."""
    logger.info("Testing audio narration flow...")
    
    # Run the tests
    test1 = await test_audio_processing_marker()
    test2 = await test_narrated_video_priority()
    
    # Print summary
    if test1 and test2:
        logger.info("✅ All tests passed! The audio narration flow works correctly.")
    else:
        logger.error("❌ Some tests failed. The audio narration flow may not be working correctly.")

if __name__ == "__main__":
    asyncio.run(main()) 