"""
Media processing service for merging audio and video.
"""
import os
import logging
import asyncio
import json
import tempfile
import shutil
from pathlib import Path
from typing import Optional, Dict, Any, List, Union
import ffmpeg

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the directory for storing temporary files
TEMP_DIR = Path("./temp")
os.makedirs(TEMP_DIR, exist_ok=True)

async def merge_audio_video(
    video_path: Union[str, Path],
    audio_path: Union[str, Path],
    output_path: Optional[Union[str, Path]] = None,
    overwrite: bool = True
) -> Optional[Path]:
    """
    Merge audio and video files using FFmpeg.
    
    Args:
        video_path: Path to the video file
        audio_path: Path to the audio file
        output_path: Path to save the output file (if None, a path will be generated)
        overwrite: Whether to overwrite the output file if it exists
        
    Returns:
        Path to the merged video file or None if merging failed
    """
    # Convert paths to Path objects
    video_path = Path(video_path)
    audio_path = Path(audio_path)
    
    # Generate output path if not provided
    if output_path is None:
        output_path = video_path.parent / f"{video_path.stem}_with_audio{video_path.suffix}"
    else:
        output_path = Path(output_path)
    
    # Create parent directory if it doesn't exist
    os.makedirs(output_path.parent, exist_ok=True)
    
    try:
        logger.info(f"Merging video {video_path} with audio {audio_path}")
        
        # Check if files exist
        if not video_path.exists():
            logger.error(f"Video file {video_path} does not exist")
            return None
        
        if not audio_path.exists():
            logger.error(f"Audio file {audio_path} does not exist")
            return None
        
        # Build the FFmpeg command
        ffmpeg_cmd = (
            ffmpeg
            .input(str(video_path))
            .output(str(output_path), acodec='copy', vcodec='copy', map=0)
            .global_args('-y' if overwrite else None)
        )
        
        # Run the FFmpeg command asynchronously
        await asyncio.to_thread(
            ffmpeg_cmd.run,
            capture_stdout=True,
            capture_stderr=True
        )
        
        logger.info(f"Video and audio merged successfully to {output_path}")
        return output_path
    
    except ffmpeg.Error as e:
        logger.error(f"FFmpeg error: {e.stderr.decode() if e.stderr else str(e)}")
        return None
    
    except Exception as e:
        logger.error(f"Error merging audio and video: {str(e)}")
        return None

async def merge_audio_segments_with_video(
    video_path: Union[str, Path],
    audio_manifest: Dict[str, Any],
    output_path: Optional[Union[str, Path]] = None,
    overwrite: bool = True
) -> Optional[Path]:
    """
    Merge multiple audio segments with a video using FFmpeg.
    
    Args:
        video_path: Path to the video file
        audio_manifest: Audio manifest with paths to audio segments
        output_path: Path to save the output file (if None, a path will be generated)
        overwrite: Whether to overwrite the output file if it exists
        
    Returns:
        Path to the merged video file or None if merging failed
    """
    # Convert paths to Path objects
    video_path = Path(video_path)
    
    # Generate output path if not provided
    if output_path is None:
        output_path = video_path.parent / f"{video_path.stem}_with_audio{video_path.suffix}"
    else:
        output_path = Path(output_path)
    
    # Create parent directory if it doesn't exist
    os.makedirs(output_path.parent, exist_ok=True)
    
    try:
        logger.info(f"Merging video {video_path} with audio segments")
        
        # Check if video file exists
        if not video_path.exists():
            logger.error(f"Video file {video_path} does not exist")
            return None
        
        # Create a temporary directory for processing
        with tempfile.TemporaryDirectory(dir=TEMP_DIR) as temp_dir:
            temp_dir_path = Path(temp_dir)
            
            # First, concatenate all audio segments into a single file
            audio_segments = audio_manifest.get("segments", [])
            
            if not audio_segments:
                logger.error("No audio segments found in manifest")
                return None
            
            # Create a temporary file for the concatenated audio
            concat_audio_path = temp_dir_path / "concatenated_audio.mp3"
            
            # Create a file with a list of audio files to concatenate
            concat_list_path = temp_dir_path / "concat_list.txt"
            with open(concat_list_path, "w") as f:
                for segment in audio_segments:
                    audio_path = segment.get("audio_path")
                    if audio_path and Path(audio_path).exists():
                        f.write(f"file '{audio_path}'\n")
            
            # Concatenate the audio files
            concat_cmd = (
                ffmpeg
                .input(str(concat_list_path), format="concat", safe=0)
                .output(str(concat_audio_path), c="copy")
                .global_args('-y')
            )
            
            # Run the concatenation command
            await asyncio.to_thread(
                concat_cmd.run,
                capture_stdout=True,
                capture_stderr=True
            )
            
            # Now merge the concatenated audio with the video
            merge_cmd = (
                ffmpeg
                .input(str(video_path))
                .input(str(concat_audio_path))
                .output(
                    str(output_path),
                    vcodec="copy",
                    acodec="aac",
                    map=["0:v", "1:a"],
                    shortest=None
                )
                .global_args('-y' if overwrite else None)
            )
            
            # Run the merge command
            await asyncio.to_thread(
                merge_cmd.run,
                capture_stdout=True,
                capture_stderr=True
            )
            
            logger.info(f"Video and audio segments merged successfully to {output_path}")
            return output_path
    
    except ffmpeg.Error as e:
        logger.error(f"FFmpeg error: {e.stderr.decode() if e.stderr else str(e)}")
        return None
    
    except Exception as e:
        logger.error(f"Error merging audio segments with video: {str(e)}")
        return None

async def process_video_with_narration(
    video_id: str,
    video_path: Union[str, Path],
    script: List[Dict[str, Any]],
    voice_id: Optional[str] = None,
    output_path: Optional[Union[str, Path]] = None
) -> Optional[Path]:
    """
    Process a video with narration.
    
    Args:
        video_id: The ID of the video
        video_path: Path to the video file
        script: List of script segments with text and timing information
        voice_id: The ID of the voice to use
        output_path: Path to save the output file (if None, a path will be generated)
        
    Returns:
        Path to the processed video file or None if processing failed
    """
    from app.services.tts import generate_audio_for_script, DEFAULT_VOICE_ID
    
    try:
        # Use default voice ID if none provided
        if voice_id is None:
            voice_id = DEFAULT_VOICE_ID
            logger.info(f"No voice ID provided, using default voice: {voice_id}")
        
        # Generate audio for the script
        audio_manifest = await generate_audio_for_script(script, video_id, voice_id)
        
        if not audio_manifest or not audio_manifest.get("segments"):
            logger.error(f"Failed to generate audio for video {video_id}")
            return None
        
        # Merge audio with video
        result_path = await merge_audio_segments_with_video(
            video_path=video_path,
            audio_manifest=audio_manifest,
            output_path=output_path
        )
        
        return result_path
    
    except Exception as e:
        logger.error(f"Error processing video with narration: {str(e)}")
        return None
