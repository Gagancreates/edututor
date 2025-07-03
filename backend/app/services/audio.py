"""
Audio processing and synchronization service.
"""
import os
import logging
import traceback
import asyncio
import subprocess
from typing import Optional, Dict, Any, List
from pathlib import Path

import ffmpeg

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AudioProcessor:
    """
    Handles audio processing and synchronization with videos.
    """
    
    @staticmethod
    async def merge_audio_video(
        video_path: str, 
        audio_path: str, 
        output_path: str,
        audio_delay: float = 0.0
    ) -> Optional[str]:
        """
        Merge audio and video files using FFmpeg.
        
        Args:
            video_path: Path to the video file
            audio_path: Path to the audio file
            output_path: Path for the output file
            audio_delay: Delay in seconds before starting the audio
            
        Returns:
            Path to the merged file or None if failed
        """
        try:
            logger.info(f"Merging video {video_path} with audio {audio_path}")
            
            # Ensure the output directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Build the FFmpeg command
            cmd = [
                "ffmpeg",
                "-y",  # Overwrite output file if it exists
                "-i", video_path,  # Input video
                "-i", audio_path,  # Input audio
                "-filter_complex", f"[1:a]adelay={int(audio_delay*1000)}|{int(audio_delay*1000)}[a]",  # Delay audio if needed
                "-map", "0:v",  # Map video from first input
                "-map", "[a]",  # Map delayed audio
                "-c:v", "copy",  # Copy video codec
                "-c:a", "aac",  # Use AAC for audio
                "-shortest",  # Finish encoding when the shortest input stream ends
                output_path
            ]
            
            # Run FFmpeg
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                logger.error(f"FFmpeg error: {stderr.decode()}")
                raise RuntimeError(f"FFmpeg failed with return code {process.returncode}")
            
            logger.info(f"Successfully merged video and audio to {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error merging audio and video: {str(e)}")
            logger.error(traceback.format_exc())
            return None
    
    @staticmethod
    async def get_video_duration(video_path: str) -> Optional[float]:
        """
        Get the duration of a video file.
        
        Args:
            video_path: Path to the video file
            
        Returns:
            Duration in seconds or None if failed
        """
        try:
            probe = ffmpeg.probe(video_path)
            video_info = next(s for s in probe['streams'] if s['codec_type'] == 'video')
            return float(video_info['duration'])
        except Exception as e:
            logger.error(f"Error getting video duration: {str(e)}")
            return None
    
    @staticmethod
    async def get_audio_duration(audio_path: str) -> Optional[float]:
        """
        Get the duration of an audio file.
        
        Args:
            audio_path: Path to the audio file
            
        Returns:
            Duration in seconds or None if failed
        """
        try:
            probe = ffmpeg.probe(audio_path)
            audio_info = next(s for s in probe['streams'] if s['codec_type'] == 'audio')
            return float(audio_info['duration'])
        except Exception as e:
            logger.error(f"Error getting audio duration: {str(e)}")
            return None
    
    @staticmethod
    async def adjust_audio_speed(
        audio_path: str, 
        output_path: str, 
        speed_factor: float
    ) -> Optional[str]:
        """
        Adjust the speed of an audio file.
        
        Args:
            audio_path: Path to the audio file
            output_path: Path for the output file
            speed_factor: Speed adjustment factor (1.0 = normal speed)
            
        Returns:
            Path to the adjusted file or None if failed
        """
        try:
            logger.info(f"Adjusting audio speed by factor {speed_factor}")
            
            # Ensure the output directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Build the FFmpeg command
            cmd = [
                "ffmpeg",
                "-y",  # Overwrite output file if it exists
                "-i", audio_path,  # Input audio
                "-filter:a", f"atempo={speed_factor}",  # Speed adjustment
                "-vn",  # No video
                output_path
            ]
            
            # Run FFmpeg
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                logger.error(f"FFmpeg error: {stderr.decode()}")
                raise RuntimeError(f"FFmpeg failed with return code {process.returncode}")
            
            logger.info(f"Successfully adjusted audio speed to {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error adjusting audio speed: {str(e)}")
            logger.error(traceback.format_exc())
            return None
    
    @staticmethod
    async def sync_audio_to_video(
        video_path: str, 
        audio_path: str, 
        output_path: str
    ) -> Optional[str]:
        """
        Synchronize audio with video by adjusting audio speed if necessary.
        
        Args:
            video_path: Path to the video file
            audio_path: Path to the audio file
            output_path: Path for the output file
            
        Returns:
            Path to the synchronized file or None if failed
        """
        try:
            # Get durations
            video_duration = await AudioProcessor.get_video_duration(video_path)
            audio_duration = await AudioProcessor.get_audio_duration(audio_path)
            
            if not video_duration or not audio_duration:
                raise ValueError("Could not determine video or audio duration")
            
            logger.info(f"Video duration: {video_duration}s, Audio duration: {audio_duration}s")
            
            # If durations are close enough (within 2 seconds), just merge them
            if abs(video_duration - audio_duration) < 2.0:
                logger.info("Durations are close enough, merging without adjustment")
                return await AudioProcessor.merge_audio_video(video_path, audio_path, output_path)
            
            # If audio is too long, speed it up
            if audio_duration > video_duration:
                speed_factor = audio_duration / video_duration
                logger.info(f"Audio is longer than video, speeding up by factor {speed_factor}")
                
                # Adjust audio speed
                temp_audio_path = os.path.join(os.path.dirname(output_path), "temp_adjusted_audio.mp3")
                adjusted_audio = await AudioProcessor.adjust_audio_speed(audio_path, temp_audio_path, speed_factor)
                
                if not adjusted_audio:
                    raise ValueError("Failed to adjust audio speed")
                
                # Merge with video
                result = await AudioProcessor.merge_audio_video(video_path, adjusted_audio, output_path)
                
                # Clean up temporary file
                try:
                    os.remove(temp_audio_path)
                except:
                    pass
                
                return result
            
            # If audio is too short, slow it down
            else:
                speed_factor = audio_duration / video_duration
                logger.info(f"Audio is shorter than video, slowing down by factor {speed_factor}")
                
                # Adjust audio speed
                temp_audio_path = os.path.join(os.path.dirname(output_path), "temp_adjusted_audio.mp3")
                adjusted_audio = await AudioProcessor.adjust_audio_speed(audio_path, temp_audio_path, speed_factor)
                
                if not adjusted_audio:
                    raise ValueError("Failed to adjust audio speed")
                
                # Merge with video
                result = await AudioProcessor.merge_audio_video(video_path, adjusted_audio, output_path)
                
                # Clean up temporary file
                try:
                    os.remove(temp_audio_path)
                except:
                    pass
                
                return result
            
        except Exception as e:
            logger.error(f"Error synchronizing audio and video: {str(e)}")
            logger.error(traceback.format_exc())
            return None