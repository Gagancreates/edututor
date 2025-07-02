"""
Helper functions for the application.
"""
import os
import re
import uuid
import glob
from pathlib import Path
from typing import List, Optional, Dict, Any, Union

def generate_uuid() -> str:
    """
    Generate a unique identifier for a video.
    
    Returns:
        A unique identifier string
    """
    return str(uuid.uuid4())

def clean_code(code_text: str) -> str:
    """
    Clean the code text by removing any Markdown formatting.
    
    Args:
        code_text: The code text to clean
        
    Returns:
        Cleaned code text
    """
    # Remove Markdown code block markers (```python and ```)
    code_text = re.sub(r'^```python\s*', '', code_text, flags=re.MULTILINE)
    code_text = re.sub(r'^```\s*$', '', code_text, flags=re.MULTILINE)
    
    # Remove any other Markdown formatting that might be present
    code_text = re.sub(r'^```.*\s*', '', code_text, flags=re.MULTILINE)
    
    return code_text.strip()

def find_video_files(directory: Union[str, Path]) -> List[Path]:
    """
    Find all video files in a directory and its subdirectories.
    
    Args:
        directory: The directory to search
        
    Returns:
        List of paths to video files
    """
    if isinstance(directory, str):
        directory = Path(directory)
    
    video_files = []
    
    # Check the main directory
    video_files.extend(list(directory.glob("*.mp4")))
    
    # Check for the default Manim media structure
    media_dir = directory / "videos"
    if media_dir.exists():
        # Check all quality subdirectories (480p15, 720p30, 1080p60, etc.)
        for quality_dir in media_dir.iterdir():
            if quality_dir.is_dir():
                video_files.extend(list(quality_dir.glob("*.mp4")))
                
                # Check for partial movie files directory
                partial_dir = quality_dir / "partial_movie_files"
                if partial_dir.exists():
                    for scene_dir in partial_dir.iterdir():
                        if scene_dir.is_dir():
                            video_files.extend(list(scene_dir.glob("*.mp4")))
    
    # Check for media_dir structure
    media_dir = directory / "media" / "videos"
    if media_dir.exists():
        for quality_dir in media_dir.iterdir():
            if quality_dir.is_dir():
                video_files.extend(list(quality_dir.glob("*.mp4")))
                
                # Check for partial movie files directory
                partial_dir = quality_dir / "partial_movie_files"
                if partial_dir.exists():
                    for scene_dir in partial_dir.iterdir():
                        if scene_dir.is_dir():
                            video_files.extend(list(scene_dir.glob("*.mp4")))
    
    # Check for the temp directory structure that might be used
    for temp_dir in directory.glob("**/videos"):
        if temp_dir.is_dir():
            for quality_dir in temp_dir.iterdir():
                if quality_dir.is_dir():
                    video_files.extend(list(quality_dir.glob("*.mp4")))
                    
                    # Check for partial movie files directory
                    partial_dir = quality_dir / "partial_movie_files"
                    if partial_dir.exists():
                        for scene_dir in partial_dir.iterdir():
                            if scene_dir.is_dir():
                                video_files.extend(list(scene_dir.glob("*.mp4")))
    
    return video_files

def get_video_path(video_id: str) -> Optional[str]:
    """
    Get the path to a generated video.
    
    Args:
        video_id: The ID of the video
        
    Returns:
        The path to the video file, or None if not found
    """
    # Define the videos directory
    videos_dir = Path("./videos")
    
    # Check if the video directory exists
    video_dir = videos_dir / video_id
    if not video_dir.exists():
        return None
    
    # First check for a direct MP4 file with the same name as the video_id
    direct_video_path = video_dir / f"{video_id}.mp4"
    if direct_video_path.exists():
        return str(direct_video_path)
    
    # If direct file not found, search for any video files in the directory
    video_files = find_video_files(video_dir)
    
    # If we found video files, return the path to the first one
    if video_files:
        return str(video_files[0])
    
    return None

def get_video_status(video_id: str) -> Dict[str, Any]:
    """
    Get the status of a video generation process.
    
    Args:
        video_id: The ID of the video
        
    Returns:
        Dictionary with status information
    """
    # Define the videos directory
    videos_dir = Path("./videos")
    
    # Check if the video directory exists
    video_dir = videos_dir / video_id
    if not video_dir.exists():
        return {
            "video_id": video_id,
            "status": "not_found",
            "message": "Video ID not found"
        }
    
    # Check if there's an error file
    error_path = video_dir / "error.txt"
    if error_path.exists():
        try:
            with open(error_path, "r", encoding="utf-8") as f:
                error_message = f.read()
                # Get just the first line for a cleaner error message
                error_message = error_message.split('\n')[0]
        except Exception as e:
            error_message = "An error occurred during video generation"
        
        return {
            "video_id": video_id,
            "status": "failed",  # Changed from "error" to match frontend expectations
            "message": error_message
        }
    
    # First check for a direct MP4 file with the same name as the video_id
    direct_video_path = video_dir / f"{video_id}.mp4"
    if direct_video_path.exists():
        return {
            "video_id": video_id,
            "status": "completed",
            "message": "Video generation completed",
            "video_url": f"/api/video/{video_id}"
        }
    
    # If direct file not found, check for any video files
    video_files = find_video_files(video_dir)
    if video_files:
        return {
            "video_id": video_id,
            "status": "completed",
            "message": "Video generation completed",
            "video_url": f"/api/video/{video_id}"
        }
    
    # If there's a directory but no video file or error file, it's still processing
    return {
        "video_id": video_id,
        "status": "processing",
        "message": "Video generation in progress"
    } 