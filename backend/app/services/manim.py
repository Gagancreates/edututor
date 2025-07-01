"""
Manim code generation and execution service.
"""
import os
import tempfile
import subprocess
import asyncio
import logging
from pathlib import Path
from typing import Optional

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the directory for storing generated videos
VIDEOS_DIR = Path("./videos")
os.makedirs(VIDEOS_DIR, exist_ok=True)

async def execute_manim_code(video_id: str, manim_code: str) -> str:
    """
    Execute Manim code to generate an educational video.
    
    Args:
        video_id: Unique identifier for the video
        manim_code: The Manim Python code to execute
        
    Returns:
        Path to the generated video file
    """
    logger.info(f"Starting Manim execution for video ID: {video_id}")
    
    # Create a temporary directory for this generation
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create the Python file with the Manim code
        script_path = Path(temp_dir) / f"{video_id}.py"
        with open(script_path, "w") as f:
            f.write(manim_code)
        
        logger.info(f"Created Manim script at {script_path}")
        
        # Output directory for the video
        output_dir = VIDEOS_DIR / video_id
        os.makedirs(output_dir, exist_ok=True)
        
        try:
            # Execute Manim with the generated code
            # Note: This assumes Manim is properly installed in the environment
            cmd = [
                "manim",
                "-qm",  # Medium quality
                "--output_file", f"{video_id}",
                "--media_dir", str(output_dir),
                str(script_path),
                "CreateScene"  # Assumes the main scene class is named CreateScene
            ]
            
            logger.info(f"Executing Manim command: {' '.join(cmd)}")
            
            # Run the command with a timeout
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=300)  # 5-minute timeout
            
            if process.returncode != 0:
                error_message = stderr.decode()
                logger.error(f"Manim execution failed: {error_message}")
                raise RuntimeError(f"Manim execution failed: {error_message}")
            
            # Find the generated video file
            video_files = list(output_dir.glob("*.mp4"))
            if not video_files:
                logger.error("No video file was generated")
                raise FileNotFoundError("No video file was generated")
            
            # Return the path to the video file
            video_path = str(video_files[0])
            logger.info(f"Successfully generated video at {video_path}")
            return video_path
            
        except asyncio.TimeoutError:
            logger.error(f"Manim execution timed out for video ID: {video_id}")
            error_path = output_dir / "error.txt"
            with open(error_path, "w") as f:
                f.write("Error generating video: Execution timed out after 5 minutes")
            raise RuntimeError("Manim execution timed out after 5 minutes")
            
        except Exception as e:
            # Create an error file to indicate failure
            logger.error(f"Error during Manim execution: {str(e)}")
            error_path = output_dir / "error.txt"
            with open(error_path, "w") as f:
                f.write(f"Error generating video: {str(e)}")
            raise 