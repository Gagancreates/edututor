"""
Helper utility functions for the EduTutor application.
"""
import uuid
import os
from pathlib import Path
from typing import Dict, Any, Optional

def generate_unique_id() -> str:
    """
    Generate a unique identifier for videos and other resources.
    
    Returns:
        A unique string ID
    """
    return str(uuid.uuid4())

def get_video_path(video_id: str) -> Optional[Path]:
    """
    Get the path to a generated video file.
    
    Args:
        video_id: The unique ID of the video
        
    Returns:
        Path to the video file if it exists, None otherwise
    """
    videos_dir = Path("./videos") / video_id
    if not videos_dir.exists():
        return None
    
    # Look for MP4 files
    video_files = list(videos_dir.glob("*.mp4"))
    if not video_files:
        return None
    
    return video_files[0]

def get_video_status(video_id: str) -> Dict[str, Any]:
    """
    Get the status of a video generation request.
    
    Args:
        video_id: The unique ID of the video
        
    Returns:
        Dictionary with status information
    """
    videos_dir = Path("./videos") / video_id
    
    # Check if the directory exists
    if not videos_dir.exists():
        return {
            "video_id": video_id,
            "status": "not_found",
            "message": "Video not found",
            "url": None
        }
    
    # Check for error file
    error_file = videos_dir / "error.txt"
    if error_file.exists():
        with open(error_file, "r") as f:
            error_message = f.read()
        return {
            "video_id": video_id,
            "status": "failed",
            "message": error_message,
            "url": None
        }
    
    # Check for video file
    video_path = get_video_path(video_id)
    if video_path:
        return {
            "video_id": video_id,
            "status": "completed",
            "message": "Video generation completed",
            "url": f"/api/video/file/{video_id}"
        }
    
    # If directory exists but no video or error file yet, it's still processing
    return {
        "video_id": video_id,
        "status": "processing",
        "message": "Video is being generated",
        "url": None
    } 