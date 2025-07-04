"""
Test script to verify that the system is correctly prioritizing narrated videos.
"""
import os
import sys
import shutil
import logging
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
from app.utils.helpers import get_video_path, get_video_status

def test_video_path_priority():
    """Test that the get_video_path function prioritizes narrated videos."""
    # Create a test video directory
    test_video_id = "test_narration_priority"
    video_dir = Path(f"./videos/{test_video_id}")
    video_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        # Create dummy video files
        original_video_path = video_dir / f"{test_video_id}.mp4"
        narrated_video_path = video_dir / f"{test_video_id}_with_audio.mp4"
        
        # Create the files
        with open(original_video_path, "wb") as f:
            f.write(b"This is a dummy original video file")
        
        with open(narrated_video_path, "wb") as f:
            f.write(b"This is a dummy narrated video file")
        
        # Test get_video_path
        video_path = get_video_path(test_video_id)
        
        # Check if the narrated video is prioritized
        is_narrated = "_with_audio" in video_path
        
        if is_narrated:
            logger.info("✅ PASS: get_video_path correctly prioritized the narrated video")
        else:
            logger.error("❌ FAIL: get_video_path returned the original video instead of the narrated one")
        
        # Test get_video_status
        status = get_video_status(test_video_id)
        
        # Check if the status indicates narration
        has_audio = status.get("has_audio", False)
        
        if has_audio:
            logger.info("✅ PASS: get_video_status correctly indicated that the video has audio")
        else:
            logger.error("❌ FAIL: get_video_status did not indicate that the video has audio")
        
        return is_narrated and has_audio
    
    finally:
        # Clean up
        if video_dir.exists():
            shutil.rmtree(video_dir)
            logger.info(f"Cleaned up test directory {video_dir}")

def test_random_video_files():
    """Test that the system can find narrated videos even with random filenames."""
    # Create a test video directory
    test_video_id = "test_random_files"
    video_dir = Path(f"./videos/{test_video_id}")
    video_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        # Create dummy video files with random names
        original_video_path = video_dir / "random_video.mp4"
        narrated_video_path = video_dir / "random_video_with_audio.mp4"
        
        # Create the files
        with open(original_video_path, "wb") as f:
            f.write(b"This is a dummy original video file")
        
        with open(narrated_video_path, "wb") as f:
            f.write(b"This is a dummy narrated video file")
        
        # Test get_video_path
        video_path = get_video_path(test_video_id)
        
        # Check if the narrated video is prioritized
        is_narrated = "_with_audio" in video_path
        
        if is_narrated:
            logger.info("✅ PASS: get_video_path correctly prioritized the narrated video with random filename")
        else:
            logger.error("❌ FAIL: get_video_path returned the original video instead of the narrated one")
        
        # Test get_video_status
        status = get_video_status(test_video_id)
        
        # Check if the status indicates narration
        has_audio = status.get("has_audio", False)
        
        if has_audio:
            logger.info("✅ PASS: get_video_status correctly indicated that the video has audio")
        else:
            logger.error("❌ FAIL: get_video_status did not indicate that the video has audio")
        
        return is_narrated and has_audio
    
    finally:
        # Clean up
        if video_dir.exists():
            shutil.rmtree(video_dir)
            logger.info(f"Cleaned up test directory {video_dir}")

def main():
    """Run the tests."""
    logger.info("Testing video serving prioritization...")
    
    # Run the tests
    test1 = test_video_path_priority()
    test2 = test_random_video_files()
    
    # Print summary
    if test1 and test2:
        logger.info("✅ All tests passed! The system correctly prioritizes narrated videos.")
    else:
        logger.error("❌ Some tests failed. The system may not be correctly prioritizing narrated videos.")

if __name__ == "__main__":
    main() 