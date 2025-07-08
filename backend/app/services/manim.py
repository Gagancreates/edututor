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

from app.utils.helpers import find_video_files, create_audio_processing_marker, remove_audio_processing_marker

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

def clean_code(code_text: str) -> str:
    """
    Clean Manim code by removing Markdown formatting.
    
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
    Check for common errors in Manim code.
    
    Args:
        code_text: The code text to check
        
    Returns:
        Tuple of (has_errors, error_message)
    """
    for pattern, message in COMMON_MANIM_ERRORS:
        if re.search(pattern, code_text):
            return True, message
    
    return False, ""

def find_video_files(directory: Path) -> List[Path]:
    """
    Find video files in a directory.
    
    Args:
        directory: The directory to search
        
    Returns:
        List of paths to video files
    """
    # Find all MP4 files in the directory and its subdirectories
    video_files = list(directory.glob("**/*.mp4"))
    
    logger.info(f"Found {len(video_files)} video files in {directory}")
    for video_file in video_files:
        logger.info(f"Found video file: {video_file}")
    
    return video_files

def find_and_copy_video(temp_dir: str, output_dir: Path, video_id: str) -> Optional[str]:
    """
    Find and copy video files from the temporary directory to the output directory.
    
    Args:
        temp_dir: The temporary directory where Manim was executed
        output_dir: The output directory to copy videos to
        video_id: The video ID
        
    Returns:
        Path to the copied video file or None if no video was found
    """
    # First check the most likely location based on Manim's output structure
    temp_media_dir = Path(temp_dir) / "media"
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
    
    return None

def create_error_files(video_id: str, error_message: str):
    """Create error files in the video directory"""
    output_dir = Path("videos") / video_id
    os.makedirs(output_dir, exist_ok=True)
    
    error_path = output_dir / "error.txt"
    try:
        with open(error_path, "w", encoding="utf-8") as f:
            f.write(f"{error_message}\n\n")
            f.write(traceback.format_exc())
    except UnicodeEncodeError:
        with open(error_path, "w", encoding="utf-8", errors="replace") as f:
            f.write(f"{error_message}\n\n")
            f.write("[Some characters were replaced due to encoding issues]")

async def execute_manim_code_without_audio(video_id: str, manim_code: str) -> str:
    """
    Execute Manim code to generate a video without audio processing.
    This is a modified version of execute_manim_code that skips the audio generation step.
    
    Args:
        video_id: Unique identifier for the video
        manim_code: The Manim Python code to execute
        
    Returns:
        Path to the generated video file
    """
    logger.info(f"Starting Manim execution for video ID: {video_id} (without audio)")
    
    # Double-check for Markdown formatting and clean it if necessary
    if "```" in manim_code:
        logger.warning("Detected Markdown code blocks in the code, cleaning...")
        manim_code = clean_code(manim_code)
    
    # Check for common errors before execution
    has_errors, error_message = check_for_common_errors(manim_code)
    if has_errors:
        logger.error(f"Code validation failed: {error_message}")
        create_error_files(video_id, f"Code validation failed: {error_message}")
        raise ValueError(f"Code validation failed: {error_message}")
    
    # Output directory for the video
    output_dir = VIDEOS_DIR / video_id
    os.makedirs(output_dir, exist_ok=True)
    
    # Create a temporary directory for this generation
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create the Python file with the Manim code
        script_path = Path(temp_dir) / f"{video_id}.py"
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(manim_code)
        
        logger.info(f"Created Manim script at {script_path}")
        logger.info(f"Script content preview:\n{manim_code[:500]}...")
        
        # Save the script for debugging purposes
        debug_script_path = output_dir / f"{video_id}.py"
        with open(debug_script_path, "w", encoding="utf-8") as f:
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
                "-ql",  # Low quality for faster rendering
                "--output_file", f"{video_id}",
                "--media_dir", str(temp_media_dir),
                str(script_path),
                "CreateScene"  # Assumes the main scene class is named CreateScene
            ]
            
            logger.info(f"Executing Manim command: {' '.join(cmd)}")
            
            # Run the command with a timeout using subprocess
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            try:
                stdout, stderr = process.communicate(timeout=600)  # 10-minute timeout
                
                # Log the output for debugging
                try:
                    stdout_text = stdout.decode('utf-8') if stdout else ""
                except UnicodeDecodeError:
                    stdout_text = stdout.decode('utf-8', errors='replace') if stdout else ""
                    logger.warning("Unicode decode error in stdout, some characters were replaced")
                
                try:
                    stderr_text = stderr.decode('utf-8') if stderr else ""
                except UnicodeDecodeError:
                    stderr_text = stderr.decode('utf-8', errors='replace') if stderr else ""
                    logger.warning("Unicode decode error in stderr, some characters were replaced")
                
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
                    create_error_files(video_id, f"Manim execution failed: {error_message}")
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
                
                # Find and copy video files from the temporary directory
                video_path = find_and_copy_video(temp_dir, output_dir, video_id)
                
                if video_path:
                    return video_path
                
                # If no video files were found, raise an error
                logger.error("No video files were found after Manim execution")
                create_error_files(video_id, "No video files were found after Manim execution")
                raise RuntimeError("No video files were found after Manim execution")
                
            except asyncio.TimeoutError:
                # Kill the process if it times out
                process.kill()
                logger.error("Manim execution timed out after 10 minutes")
                create_error_files(video_id, "Manim execution timed out after 10 minutes")
                raise TimeoutError("Manim execution timed out after 10 minutes")
                
        except Exception as e:
            logger.error(f"Error executing Manim code: {str(e)}")
            create_error_files(video_id, f"Error executing Manim code: {str(e)}")
            raise
    
    # This should never be reached, but just in case
    raise RuntimeError("Unexpected error in Manim execution")

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
        try:
            with open(error_path, "w", encoding="utf-8") as f:
                f.write(f"Code validation failed: {error_message}\n\n")
                f.write("Please regenerate with a simpler animation.")
        except UnicodeEncodeError:
            with open(error_path, "w", encoding="utf-8", errors="replace") as f:
                f.write(f"Code validation failed: [Some characters were replaced due to encoding issues]\n\n")
                f.write("Please regenerate with a simpler animation.")
        
        raise ValueError(f"Code validation failed: {error_message}")
    
    # Output directory for the video
    output_dir = VIDEOS_DIR / video_id
    os.makedirs(output_dir, exist_ok=True)
    
    # Extract narration text from the Manim code
    from app.services.text_extraction import extract_narration_from_manim
    script = extract_narration_from_manim(manim_code)
    
    # Save the script for reference
    script_json_path = output_dir / "script.json"
    import json
    with open(script_json_path, "w") as f:
        json.dump(script, f, indent=2)
    
    # Create a temporary directory for this generation
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create the Python file with the Manim code
        script_path = Path(temp_dir) / f"{video_id}.py"
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(manim_code)
        
        logger.info(f"Created Manim script at {script_path}")
        logger.info(f"Script content preview:\n{manim_code[:500]}...")
        
        # Save the script for debugging purposes
        debug_script_path = output_dir / f"{video_id}.py"
        with open(debug_script_path, "w", encoding="utf-8") as f:
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
                "-ql",  # Low quality for faster rendering
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
                stdout, stderr = process.communicate(timeout=600)  # 10-minute timeout
                
                # Log the output for debugging
                try:
                    stdout_text = stdout.decode('utf-8') if stdout else ""
                except UnicodeDecodeError:
                    # Handle UTF-8 decode errors by using 'replace' error handler
                    stdout_text = stdout.decode('utf-8', errors='replace') if stdout else ""
                    logger.warning("Unicode decode error in stdout, some characters were replaced")
                
                try:
                    stderr_text = stderr.decode('utf-8') if stderr else ""
                except UnicodeDecodeError:
                    # Handle UTF-8 decode errors by using 'replace' error handler
                    stderr_text = stderr.decode('utf-8', errors='replace') if stderr else ""
                    logger.warning("Unicode decode error in stderr, some characters were replaced")
                
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
                    try:
                        with open(error_path, "w", encoding="utf-8") as f:
                            f.write(f"Manim execution failed:\n{error_message}")
                    except UnicodeEncodeError:
                        # If we can't write with UTF-8, try with a more permissive encoding
                        with open(error_path, "w", encoding="utf-8", errors="replace") as f:
                            f.write(f"Manim execution failed:\n[Some characters were replaced due to encoding issues]")
                            f.write(f"\nReturn code: {process.returncode}")
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
                    
                    # Set the audio processing marker to indicate that audio processing is starting
                    create_audio_processing_marker(video_id)
                    
                    # Generate audio and merge with video
                    from app.services.media_processing import process_video_with_narration
                    narrated_video_path = await process_video_with_narration(
                        video_id=video_id,
                        video_path=dest_path,
                        script=script
                    )
                    
                    if narrated_video_path:
                        logger.info(f"Generated narrated video at {narrated_video_path}")
                        # Replace the original video with the narrated one
                        shutil.copy2(narrated_video_path, dest_path)
                        logger.info(f"Replaced original video with narrated version")
                    else:
                        logger.warning(f"Failed to generate narrated video, using original video")
                    
                    # Remove the audio processing marker regardless of success or failure
                    remove_audio_processing_marker(video_id)
                    
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
                        
                        # Set the audio processing marker to indicate that audio processing is starting
                        create_audio_processing_marker(video_id)
                        
                        # Generate audio and merge with video
                        from app.services.media_processing import process_video_with_narration
                        narrated_video_path = await process_video_with_narration(
                            video_id=video_id,
                            video_path=dest_path,
                            script=script
                        )
                        
                        if narrated_video_path:
                            logger.info(f"Generated narrated video at {narrated_video_path}")
                            # Replace the original video with the narrated one
                            shutil.copy2(narrated_video_path, dest_path)
                            logger.info(f"Replaced original video with narrated version")
                        else:
                            logger.warning(f"Failed to generate narrated video, using original video")
                        
                        # Remove the audio processing marker regardless of success or failure
                        remove_audio_processing_marker(video_id)
                        
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
                    
                    # Set the audio processing marker to indicate that audio processing is starting
                    create_audio_processing_marker(video_id)
                    
                    # Generate audio and merge with video
                    from app.services.media_processing import process_video_with_narration
                    narrated_video_path = await process_video_with_narration(
                        video_id=video_id,
                        video_path=result_video,
                        script=script
                    )
                    
                    if narrated_video_path:
                        logger.info(f"Generated narrated video at {narrated_video_path}")
                        # Replace the original video with the narrated one
                        shutil.copy2(narrated_video_path, result_video)
                        logger.info(f"Replaced original video with narrated version")
                    else:
                        logger.warning(f"Failed to generate narrated video, using original video")
                    
                    # Remove the audio processing marker regardless of success or failure
                    remove_audio_processing_marker(video_id)
                    
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
                            
                            # Set the audio processing marker to indicate that audio processing is starting
                            create_audio_processing_marker(video_id)
                            
                            # Generate audio and merge with video
                            from app.services.media_processing import process_video_with_narration
                            narrated_video_path = await process_video_with_narration(
                                video_id=video_id,
                                video_path=result_video,
                                script=script
                            )
                            
                            if narrated_video_path:
                                logger.info(f"Generated narrated video at {narrated_video_path}")
                                # Replace the original video with the narrated one
                                shutil.copy2(narrated_video_path, result_video)
                                logger.info(f"Replaced original video with narrated version")
                            else:
                                logger.warning(f"Failed to generate narrated video, using original video")
                            
                            # Remove the audio processing marker regardless of success or failure
                            remove_audio_processing_marker(video_id)
                            
                            return str(result_video)
                
                # Last resort: Use glob to find any MP4 files
                all_mp4_files = list(Path(".").glob("**/*.mp4"))
                
                if all_mp4_files:
                    logger.info(f"Found {len(all_mp4_files)} MP4 files using glob search")
                    for mp4_file in all_mp4_files:
                        logger.info(f"Found MP4 file: {mp4_file}")
                        dest_path = output_dir / mp4_file.name
                        shutil.copy2(mp4_file, dest_path)
                        logger.info(f"Copied video from {mp4_file} to {dest_path}")
                    
                    # Return the path to the first video file
                    result_video = output_dir / all_mp4_files[0].name
                    
                    # Set the audio processing marker to indicate that audio processing is starting
                    create_audio_processing_marker(video_id)
                    
                    # Generate audio and merge with video
                    from app.services.media_processing import process_video_with_narration
                    narrated_video_path = await process_video_with_narration(
                        video_id=video_id,
                        video_path=result_video,
                        script=script
                    )
                    
                    if narrated_video_path:
                        logger.info(f"Generated narrated video at {narrated_video_path}")
                        # Replace the original video with the narrated one
                        shutil.copy2(narrated_video_path, result_video)
                        logger.info(f"Replaced original video with narrated version")
                    else:
                        logger.warning(f"Failed to generate narrated video, using original video")
                    
                    # Remove the audio processing marker regardless of success or failure
                    remove_audio_processing_marker(video_id)
                    
                    return str(result_video)
                
                # Remove the audio processing marker since no video was found
                remove_audio_processing_marker(video_id)
                
                # Create a dummy file to indicate that the video should exist
                dummy_path = output_dir / f"{video_id}_dummy.mp4"
                with open(dummy_path, "w", encoding="utf-8") as f:
                    f.write("This is a dummy file. The actual video was not found.")
                
                logger.error("No video file was found. Created a dummy file instead.")
                error_path = output_dir / "error.txt"
                try:
                    with open(error_path, "w", encoding="utf-8") as f:
                        f.write("Error: No video file was found, but Manim reported success.")
                except UnicodeEncodeError:
                    with open(error_path, "w", encoding="utf-8", errors="replace") as f:
                        f.write("Error: No video file was found, but Manim reported success.")
                raise FileNotFoundError("No video file was generated, but Manim reported success.")
            
            except subprocess.TimeoutExpired:
                process.kill()
                logger.error("Manim execution timed out after 10 minutes")
                error_path = output_dir / "error.txt"
                with open(error_path, "w") as f:
                    f.write("Manim execution timed out after 10 minutes. The animation might be too complex.")
                
                # Remove the audio processing marker if it exists
                remove_audio_processing_marker(video_id)
                
                raise TimeoutError("Manim execution timed out after 10 minutes")
        
        except Exception as e:
            logger.error(f"Error executing Manim code: {str(e)}")
            logger.error(traceback.format_exc())
            error_path = output_dir / "error.txt"
            try:
                with open(error_path, "w", encoding="utf-8") as f:
                    f.write(f"Error executing Manim code: {str(e)}\n\n{traceback.format_exc()}")
            except UnicodeEncodeError:
                with open(error_path, "w", encoding="utf-8", errors="replace") as f:
                    f.write(f"Error executing Manim code: [Some characters were replaced due to encoding issues]\n\n{traceback.format_exc()}")
            raise 