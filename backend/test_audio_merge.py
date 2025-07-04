"""
Test script for audio-video merging functionality.
"""
import asyncio
import json
import os
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Import the media processing service
from app.services.media_processing import merge_audio_segments_with_video

async def test_audio_merge():
    """Test merging audio segments with a video."""
    # Define the test video ID
    video_id = "5f9fa82d-abeb-49c5-b51f-915bace130d5"
    
    # Define paths
    video_path = Path(f"videos/{video_id}/{video_id}.mp4")
    manifest_path = Path(f"audio/{video_id}/manifest.json")
    output_path = Path(f"videos/{video_id}/{video_id}_with_audio.mp4")
    
    # Check if files exist
    if not video_path.exists():
        logger.error(f"Video file not found: {video_path}")
        return
    
    if not manifest_path.exists():
        logger.error(f"Audio manifest not found: {manifest_path}")
        return
    
    # Load the audio manifest
    try:
        with open(manifest_path, "r") as f:
            audio_manifest = json.load(f)
    except Exception as e:
        logger.error(f"Error loading audio manifest: {e}")
        return
    
    # Verify audio files exist
    missing_files = []
    for segment in audio_manifest.get("segments", []):
        audio_path = segment.get("audio_path")
        if audio_path and not Path(audio_path).exists():
            missing_files.append(audio_path)
    
    if missing_files:
        logger.error(f"Missing audio files: {missing_files}")
        return
    
    # Merge audio with video
    try:
        logger.info(f"Starting audio-video merge for {video_id}")
        result_path = await merge_audio_segments_with_video(
            video_path=video_path,
            audio_manifest=audio_manifest,
            output_path=output_path
        )
        
        if result_path:
            logger.info(f"Successfully merged audio and video: {result_path}")
        else:
            logger.error("Audio-video merge failed")
    except Exception as e:
        logger.error(f"Error during audio-video merge: {e}")

if __name__ == "__main__":
    asyncio.run(test_audio_merge()) 