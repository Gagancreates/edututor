"""
Test script to verify video serving functionality.
"""
import asyncio
import logging
from pathlib import Path
import os
import sys

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add the current directory to the path so we can import app modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.utils.helpers import get_video_path, get_video_status, find_video_files

async def test_video_serving():
    """
    Test the video serving functionality.
    """
    # Get all video directories
    videos_dir = Path("./videos")
    if not videos_dir.exists():
        logger.error(f"Videos directory not found: {videos_dir}")
        return
    
    video_dirs = [d for d in videos_dir.iterdir() if d.is_dir()]
    if not video_dirs:
        logger.error("No video directories found")
        return
    
    logger.info(f"Found {len(video_dirs)} video directories")
    
    # Test each video directory
    for video_dir in video_dirs:
        video_id = video_dir.name
        logger.info(f"\nTesting video ID: {video_id}")
        
        # Test get_video_status
        status = get_video_status(video_id)
        logger.info(f"Status: {status['status']}")
        logger.info(f"Message: {status['message']}")
        
        # Test get_video_path
        video_path = get_video_path(video_id)
        if video_path:
            logger.info(f"Video path: {video_path}")
            
            # Check if the file exists
            if os.path.exists(video_path):
                file_size = os.path.getsize(video_path)
                logger.info(f"Video file exists, size: {file_size} bytes")
                
                # Check if the file is a valid MP4
                with open(video_path, 'rb') as f:
                    header = f.read(8)
                    # Simple check for MP4 file signature
                    if header[4:8] in [b'ftyp', b'moov']:
                        logger.info("✅ Valid MP4 file detected")
                    else:
                        logger.warning("⚠️ File may not be a valid MP4")
            else:
                logger.error(f"❌ Video file not found at path: {video_path}")
        else:
            logger.error(f"❌ No video path returned for ID: {video_id}")
        
        # Check direct file with video_id name
        direct_path = video_dir / f"{video_id}.mp4"
        if direct_path.exists():
            logger.info(f"✅ Direct video file exists: {direct_path}")
        else:
            logger.info(f"Direct video file does not exist: {direct_path}")
            
            # Check for other video files using find_video_files
            other_videos = find_video_files(video_dir)
            if other_videos:
                logger.info(f"Found {len(other_videos)} other video files:")
                for v in other_videos:
                    logger.info(f"  - {v}")
            else:
                logger.info("No other video files found in directory")
        
        # Check for error file
        error_path = video_dir / "error.txt"
        if error_path.exists():
            logger.info(f"Error file exists: {error_path}")
            with open(error_path, 'r') as f:
                error_content = f.read(200)  # Read first 200 chars
                logger.info(f"Error content preview: {error_content}...")
    
    logger.info("\nTest completed")

if __name__ == "__main__":
    asyncio.run(test_video_serving()) 