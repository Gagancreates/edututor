"""
Manim code generation and execution service.
"""
import os
import tempfile
import subprocess
import asyncio
from pathlib import Path
from typing import Optional

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
    # Create a temporary directory for this generation
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create the Python file with the Manim code
        script_path = Path(temp_dir) / f"{video_id}.py"
        with open(script_path, "w") as f:
            f.write(manim_code)
        
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
            
            # Run the command with a timeout
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=300)  # 5-minute timeout
            
            if process.returncode != 0:
                raise RuntimeError(f"Manim execution failed: {stderr.decode()}")
            
            # Find the generated video file
            video_files = list(output_dir.glob("*.mp4"))
            if not video_files:
                raise FileNotFoundError("No video file was generated")
            
            # Return the path to the video file
            video_path = str(video_files[0])
            return video_path
            
        except Exception as e:
            # Create an error file to indicate failure
            error_path = output_dir / "error.txt"
            with open(error_path, "w") as f:
                f.write(f"Error generating video: {str(e)}")
            raise 