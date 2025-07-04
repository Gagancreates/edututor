"""
Media processing service for merging audio and video.
"""
import os
import logging
import asyncio
import json
import tempfile
import shutil
import subprocess
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
        
        # Use subprocess directly for better control and error handling
        cmd = [
            "ffmpeg", "-y",
            "-i", str(video_path),
            "-i", str(audio_path),
            "-map", "0:v", "-map", "1:a",
            "-c:v", "copy", "-c:a", "aac",
            str(output_path)
        ]
        
        logger.debug(f"Running FFmpeg command: {' '.join(cmd)}")
        
        # Run the FFmpeg command
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()
        
        if process.returncode != 0:
            logger.error(f"FFmpeg error: {stderr.decode()}")
            return None
        
        if not output_path.exists():
            logger.error(f"Output file was not created: {output_path}")
            return None
        
        logger.info(f"Video and audio merged successfully to {output_path}")
        return output_path
    
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
            
            # Log audio segments for debugging
            logger.debug(f"Found {len(audio_segments)} audio segments")
            for i, segment in enumerate(audio_segments):
                audio_path = segment.get("audio_path")
                exists = Path(audio_path).exists() if audio_path else False
                logger.debug(f"Segment {i}: {audio_path} (exists: {exists})")
            
            # Create a file with a list of audio files to concatenate
            concat_list_path = temp_dir_path / "concat_list.txt"
            valid_segments = 0
            
            with open(concat_list_path, "w") as f:
                for segment in audio_segments:
                    audio_path = segment.get("audio_path")
                    if audio_path and Path(audio_path).exists():
                        # Use absolute paths in the concat file
                        abs_path = Path(audio_path).absolute()
                        f.write(f"file '{abs_path}'\n")
                        valid_segments += 1
            
            if valid_segments == 0:
                logger.error("No valid audio segments found")
                return None
            
            logger.info(f"Created concat list with {valid_segments} valid audio segments")
            
            # Create a temporary file for the concatenated audio
            concat_audio_path = temp_dir_path / "concatenated_audio.mp3"
            
            # Use subprocess directly for the concatenation command
            concat_cmd = [
                "ffmpeg", "-y", "-f", "concat", "-safe", "0",
                "-i", str(concat_list_path),
                "-c", "copy", str(concat_audio_path)
            ]
            
            # Log the command for debugging
            logger.debug(f"Running FFmpeg concat command: {' '.join(concat_cmd)}")
            
            try:
                # Run the concatenation command
                process = await asyncio.create_subprocess_exec(
                    *concat_cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                
                stdout, stderr = await process.communicate()
                
                if process.returncode != 0:
                    logger.error(f"FFmpeg concat error: {stderr.decode()}")
                    return None
                
                # Check if concatenated audio file was created
                if not concat_audio_path.exists():
                    logger.error(f"Concatenated audio file was not created: {concat_audio_path}")
                    return None
                
                logger.info(f"Successfully concatenated audio segments to {concat_audio_path}")
                
                # Now merge the concatenated audio with the video using subprocess
                merge_cmd = [
                    "ffmpeg", "-y",
                    "-i", str(video_path),
                    "-i", str(concat_audio_path),
                    "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-c:a", "aac",
                    str(output_path)
                ]
                
                # Log the command for debugging
                logger.debug(f"Running FFmpeg merge command: {' '.join(merge_cmd)}")
                
                # Run the merge command
                process = await asyncio.create_subprocess_exec(
                    *merge_cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                
                stdout, stderr = await process.communicate()
                
                if process.returncode != 0:
                    logger.error(f"FFmpeg merge error: {stderr.decode()}")
                    return None
                
                # Check if output file was created
                if not output_path.exists():
                    logger.error(f"Output file was not created: {output_path}")
                    return None
                
                logger.info(f"Video and audio segments merged successfully to {output_path}")
                return output_path
                
            except Exception as e:
                logger.error(f"Error during FFmpeg processing: {str(e)}")
                return None
    
    except Exception as e:
        logger.error(f"Error merging audio segments with video: {str(e)}", exc_info=True)
        return None

# Alternative implementation using direct FFmpeg command execution
async def merge_audio_segments_with_video_direct(
    video_path: Union[str, Path],
    audio_manifest: Dict[str, Any],
    output_path: Optional[Union[str, Path]] = None,
    overwrite: bool = True
) -> Optional[Path]:
    """
    Alternative implementation that uses direct FFmpeg command execution.
    
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
        logger.info(f"Merging video {video_path} with audio segments using direct FFmpeg execution")
        
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
            
            # Create a file with a list of audio files to concatenate
            concat_list_path = temp_dir_path / "concat_list.txt"
            with open(concat_list_path, "w") as f:
                for segment in audio_segments:
                    audio_path = segment.get("audio_path")
                    if audio_path and Path(audio_path).exists():
                        # Use absolute paths in the concat file
                        abs_path = Path(audio_path).absolute()
                        f.write(f"file '{abs_path}'\n")
            
            # Create a temporary file for the concatenated audio
            concat_audio_path = temp_dir_path / "concatenated_audio.mp3"
            
            # Concatenate audio segments
            concat_cmd = f'ffmpeg -y -f concat -safe 0 -i "{concat_list_path}" -c copy "{concat_audio_path}"'
            logger.debug(f"Running FFmpeg concat command: {concat_cmd}")
            
            try:
                # Run the command using subprocess.run for simplicity
                process = subprocess.run(
                    concat_cmd, 
                    shell=True, 
                    check=True,
                    capture_output=True,
                    text=True
                )
            except subprocess.CalledProcessError as e:
                logger.error(f"FFmpeg concat error: {e.stderr}")
                return None
            
            # Check if concatenated audio file was created
            if not concat_audio_path.exists():
                logger.error(f"Concatenated audio file was not created: {concat_audio_path}")
                return None
            
            # Now merge the concatenated audio with the video
            merge_cmd = f'ffmpeg -y -i "{video_path}" -i "{concat_audio_path}" -map 0:v -map 1:a -c:v copy -c:a aac "{output_path}"'
            logger.debug(f"Running FFmpeg merge command: {merge_cmd}")
            
            try:
                # Run the command using subprocess.run for simplicity
                process = subprocess.run(
                    merge_cmd, 
                    shell=True, 
                    check=True,
                    capture_output=True,
                    text=True
                )
            except subprocess.CalledProcessError as e:
                logger.error(f"FFmpeg merge error: {e.stderr}")
                return None
            
            # Check if output file was created
            if not output_path.exists():
                logger.error(f"Output file was not created: {output_path}")
                return None
            
            logger.info(f"Video and audio segments merged successfully to {output_path}")
            return output_path
    
    except Exception as e:
        logger.error(f"Error merging audio segments with video: {str(e)}", exc_info=True)
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
        
        # First try the standard implementation
        result_path = await merge_audio_segments_with_video(
            video_path=video_path,
            audio_manifest=audio_manifest,
            output_path=output_path
        )
        
        # If that fails, try the alternative implementation
        if result_path is None:
            logger.warning("Standard implementation failed, trying alternative implementation")
            result_path = await merge_audio_segments_with_video_direct(
                video_path=video_path,
                audio_manifest=audio_manifest,
                output_path=output_path
            )
        
        return result_path
    
    except Exception as e:
        logger.error(f"Error processing video with narration: {str(e)}", exc_info=True)
        return None
