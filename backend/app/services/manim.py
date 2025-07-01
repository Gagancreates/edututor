"""
Manim code generation and execution service.
"""
import os
import tempfile
import subprocess
import asyncio
import logging
import sys
import traceback
import re
import glob
import shutil
from pathlib import Path
from typing import Optional, List, Tuple

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the directory for storing generated videos
VIDEOS_DIR = Path("./videos")
os.makedirs(VIDEOS_DIR, exist_ok=True)

# Common Manim errors to check for
COMMON_MANIM_ERRORS = [
    (r"TypeError: .*__init__\(\) got an unexpected keyword argument 'display_frame'", 
     "The code uses 'display_frame' parameter which is not supported in this version of Manim. Use only basic Scene class without custom parameters."),
    
    (r"AttributeError: .*object has no attribute 'tex_string'", 
     "The code tries to access 'tex_string' attribute on a non-Tex object. Only use TransformMatchingTex with Tex or MathTex objects."),
    
    (r"ZoomedScene", 
     "The code uses ZoomedScene which can cause compatibility issues. Use only the basic Scene class."),
    
    (r"ThreeDScene", 
     "The code uses ThreeDScene which can cause compatibility issues. Use only the basic Scene class."),
    
    (r"ImportError: cannot import name", 
     "The code tries to import a class or function that doesn't exist in this version of Manim."),
    
    (r"AttributeError: module 'manim' has no attribute", 
     "The code uses a feature not available in this version of Manim.")
]

def clean_code(code_text):
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

def check_for_common_errors(code_text: str) -> Tuple[bool, str]:
    """
    Check the code for common Manim errors before execution.
    
    Args:
        code_text: The Manim code to check
        
    Returns:
        Tuple of (has_errors, error_message)
    """
    # Check if the code uses any known problematic features
    for pattern, message in COMMON_MANIM_ERRORS:
        if re.search(pattern, code_text):
            return True, f"Potential error detected: {message}"
    
    # Check if the main scene class is named correctly
    if not re.search(r"class\s+CreateScene\s*\(\s*Scene\s*\)", code_text):
        return True, "The main scene class must be named 'CreateScene' and inherit from Scene"
    
    # Check for missing imports
    if not re.search(r"from\s+manim\s+import", code_text) and not re.search(r"import\s+manim", code_text):
        return True, "Missing Manim import statement"
    
    return False, ""

def find_video_files(directory: Path) -> List[Path]:
    """
    Find all video files in a directory and its subdirectories.
    
    Args:
        directory: The directory to search
        
    Returns:
        List of paths to video files
    """
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
    
    # Check for media_dir structure
    media_dir = directory / "media" / "videos"
    if media_dir.exists():
        for subdir in media_dir.iterdir():
            if subdir.is_dir():
                # Check all quality subdirectories (480p15, 720p30, 1080p60, etc.)
                for quality_dir in subdir.iterdir():
                    if quality_dir.is_dir():
                        video_files.extend(list(quality_dir.glob("*.mp4")))
    
    # Check for the temp directory structure that might be used
    for temp_dir in directory.glob("**/videos"):
        if temp_dir.is_dir():
            for quality_dir in temp_dir.iterdir():
                if quality_dir.is_dir():
                    video_files.extend(list(quality_dir.glob("*.mp4")))
    
    logger.info(f"Found {len(video_files)} video files in {directory}")
    for video_file in video_files:
        logger.info(f"Found video file: {video_file}")
    
    return video_files

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
    
    # Double-check for Markdown formatting and clean it if necessary
    if "```" in manim_code:
        logger.warning("Detected Markdown code blocks in the code, cleaning...")
        manim_code = clean_code(manim_code)
    
    # Check for common errors before execution
    has_errors, error_message = check_for_common_errors(manim_code)
    if has_errors:
        logger.error(f"Code validation failed: {error_message}")
        # Create the output directory
        output_dir = VIDEOS_DIR / video_id
        os.makedirs(output_dir, exist_ok=True)
        
        # Save the script for reference
        script_path = output_dir / f"{video_id}.py"
        with open(script_path, "w") as f:
            f.write(manim_code)
        
        # Create an error file
        error_path = output_dir / "error.txt"
        with open(error_path, "w") as f:
            f.write(f"Code validation failed: {error_message}\n\n")
            f.write("Please regenerate with a simpler animation.")
        
        raise ValueError(f"Code validation failed: {error_message}")
    
    # Output directory for the video
    output_dir = VIDEOS_DIR / video_id
    os.makedirs(output_dir, exist_ok=True)
    
    # Create a temporary directory for this generation
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create the Python file with the Manim code
        script_path = Path(temp_dir) / f"{video_id}.py"
        with open(script_path, "w") as f:
            f.write(manim_code)
        
        logger.info(f"Created Manim script at {script_path}")
        logger.info(f"Script content preview:\n{manim_code[:500]}...")
        
        # Save the script for debugging purposes
        debug_script_path = output_dir / f"{video_id}.py"
        with open(debug_script_path, "w") as f:
            f.write(manim_code)
        logger.info(f"Saved script for debugging at {debug_script_path}")
        
        try:
            # Get the path to the Python executable in the current environment
            python_executable = sys.executable
            logger.info(f"Using Python executable: {python_executable}")
            
            # Create a media directory inside the temp directory
            temp_media_dir = Path(temp_dir) / "media"
            os.makedirs(temp_media_dir, exist_ok=True)
            
            # Execute Manim using the Python module approach instead of the command
            cmd = [
                python_executable,
                "-m", "manim",
                "-qm",  # Medium quality
                "--output_file", f"{video_id}",
                "--media_dir", str(temp_media_dir),
                str(script_path),
                "CreateScene"  # Assumes the main scene class is named CreateScene
            ]
            
            logger.info(f"Executing Manim command: {' '.join(cmd)}")
            
            # Run the command with a timeout using subprocess instead of asyncio
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            try:
                stdout, stderr = process.communicate(timeout=300)  # 5-minute timeout
                
                # Log the output for debugging
                stdout_text = stdout.decode() if stdout else ""
                stderr_text = stderr.decode() if stderr else ""
                
                if stdout_text:
                    logger.info(f"Manim stdout: {stdout_text[:1000]}...")
                if stderr_text:
                    logger.error(f"Manim stderr: {stderr_text[:1000]}...")
                
                if process.returncode != 0:
                    error_message = stderr_text
                    
                    # Check for specific error patterns
                    for pattern, message in COMMON_MANIM_ERRORS:
                        if re.search(pattern, stderr_text):
                            error_message = f"Manim error: {message}\n\n{stderr_text}"
                            break
                    
                    logger.error(f"Manim execution failed with return code {process.returncode}")
                    error_path = output_dir / "error.txt"
                    with open(error_path, "w") as f:
                        f.write(f"Manim execution failed:\n{error_message}")
                    raise RuntimeError(f"Manim execution failed: {error_message}")
                
                # Extract the output path from stdout if possible
                output_path = None
                for line in stdout_text.splitlines():
                    if "File ready at" in line:
                        # Extract the path from the line
                        path_start = line.find("'")
                        if path_start != -1:
                            path_end = line.find("'", path_start + 1)
                            if path_end != -1:
                                output_path = line[path_start + 1:path_end]
                                logger.info(f"Extracted output path from stdout: {output_path}")
                                break
                
                # If we found the path in stdout, check if it exists
                if output_path and os.path.exists(output_path):
                    # Copy the video file to the output directory
                    video_file = Path(output_path)
                    dest_path = output_dir / video_file.name
                    shutil.copy2(video_file, dest_path)
                    logger.info(f"Copied video from {video_file} to {dest_path}")
                    return str(dest_path)
                
                # Search for video files in the temp_media_dir
                # First check the most likely location based on Manim's output structure
                manim_output_dir = temp_media_dir / "videos" / video_id / "720p30"
                if manim_output_dir.exists():
                    video_files = list(manim_output_dir.glob("*.mp4"))
                    if video_files:
                        # Copy the video file to the output directory
                        video_file = video_files[0]
                        dest_path = output_dir / video_file.name
                        shutil.copy2(video_file, dest_path)
                        logger.info(f"Copied video from {video_file} to {dest_path}")
                        return str(dest_path)
                
                # If not found in the expected location, do a more comprehensive search
                video_files = find_video_files(temp_media_dir)
                
                if video_files:
                    # Copy the video files to the output directory
                    for video_file in video_files:
                        dest_path = output_dir / video_file.name
                        shutil.copy2(video_file, dest_path)
                        logger.info(f"Copied video from {video_file} to {dest_path}")
                    
                    # Return the path to the first video file in the output directory
                    result_video = output_dir / video_files[0].name
                    return str(result_video)
                
                # If still no video files, check other locations
                for search_dir in [Path(temp_dir), Path.cwd(), Path("./media")]:
                    if search_dir.exists():
                        logger.info(f"Searching for videos in {search_dir}")
                        found_videos = find_video_files(search_dir)
                        if found_videos:
                            # Copy the video files to the output directory
                            for video_file in found_videos:
                                dest_path = output_dir / video_file.name
                                shutil.copy2(video_file, dest_path)
                                logger.info(f"Copied video from {video_file} to {dest_path}")
                            
                            # Return the path to the first video file in the output directory
                            result_video = output_dir / found_videos[0].name
                            return str(result_video)
                
                # If we still haven't found any videos, create a dummy video file
                if "File ready at" in stdout_text:
                    logger.warning("Manim reported a video file was created, but we couldn't find it.")
                    
                    # Save stdout and stderr to files for debugging
                    with open(output_dir / "stdout.txt", "w") as f:
                        f.write(stdout_text)
                    with open(output_dir / "stderr.txt", "w") as f:
                        f.write(stderr_text)
                    
                    # Look for any MP4 files in the entire temp directory using glob
                    all_mp4_files = list(Path(temp_dir).glob("**/*.mp4"))
                    if all_mp4_files:
                        logger.info(f"Found {len(all_mp4_files)} MP4 files using glob search")
                        for mp4_file in all_mp4_files:
                            logger.info(f"Found MP4 file: {mp4_file}")
                            dest_path = output_dir / mp4_file.name
                            shutil.copy2(mp4_file, dest_path)
                            logger.info(f"Copied video from {mp4_file} to {dest_path}")
                        
                        # Return the path to the first video file
                        result_video = output_dir / all_mp4_files[0].name
                        return str(result_video)
                    
                    # Create a dummy file to indicate that the video should exist
                    dummy_path = output_dir / f"{video_id}_dummy.mp4"
                    with open(dummy_path, "w") as f:
                        f.write("This is a dummy file. The actual video was not found.")
                    
                    logger.error("No video file was found. Created a dummy file instead.")
                    error_path = output_dir / "error.txt"
                    with open(error_path, "w") as f:
                        f.write("Error: No video file was found, but Manim reported success.")
                    raise FileNotFoundError("No video file was generated, but Manim reported success.")
                
                logger.error("No video file was generated")
                error_path = output_dir / "error.txt"
                with open(error_path, "w") as f:
                    f.write("Error: No video file was generated")
                raise FileNotFoundError("No video file was generated")
                
            except subprocess.TimeoutExpired:
                process.kill()
                logger.error(f"Manim execution timed out for video ID: {video_id}")
                error_path = output_dir / "error.txt"
                with open(error_path, "w") as f:
                    f.write("Error generating video: Execution timed out after 5 minutes")
                raise RuntimeError("Manim execution timed out after 5 minutes")
            
        except Exception as e:
            # Create an error file to indicate failure
            logger.error(f"Error during Manim execution: {str(e)}")
            logger.error(traceback.format_exc())
            error_path = output_dir / "error.txt"
            with open(error_path, "w") as f:
                f.write(f"Error generating video: {str(e)}\n\n{traceback.format_exc()}")
            raise 