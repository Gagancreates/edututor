"""
Test script for generating a simple Manim video.
"""
import os
import tempfile
import sys
import subprocess
import shutil
from pathlib import Path
import glob
import re

# Sample Manim code for testing
SAMPLE_MANIM_CODE = """
from manim import *

class CreateScene(Scene):
    def construct(self):
        # Create a circle
        circle = Circle(color=BLUE)
        self.play(Create(circle))
        
        # Create a square
        square = Square(color=RED)
        self.play(Transform(circle, square))
        
        # Add some text
        text = Text("Hello, Manim!")
        self.play(Write(text))
        
        # Move the text
        self.play(text.animate.shift(UP * 2))
        
        # Fade out everything
        self.play(FadeOut(circle), FadeOut(text))
"""

def find_video_files(directory):
    """Find video files in a directory and its subdirectories"""
    video_files = []
    
    # Check for direct mp4 files
    video_files.extend(glob.glob(os.path.join(directory, "**", "*.mp4"), recursive=True))
    
    # Print found files for debugging
    if video_files:
        print(f"Found {len(video_files)} video files:")
        for file in video_files:
            print(f"  - {file}")
    
    return video_files

def extract_output_path_from_stdout(stdout_text):
    """Extract the output path from Manim stdout"""
    for line in stdout_text.splitlines():
        if "File ready at" in line:
            # Extract the path from the line
            path_start = line.find("'")
            if path_start != -1:
                path_end = line.find("'", path_start + 1)
                if path_end != -1:
                    output_path = line[path_start + 1:path_end]
                    print(f"Extracted output path from stdout: {output_path}")
                    return output_path
    return None

def main():
    # Create a temporary directory for the test
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"Created temporary directory at {temp_dir}")
        
        # Create a Python file with the Manim code
        script_path = os.path.join(temp_dir, "test_video.py")
        with open(script_path, "w") as f:
            f.write(SAMPLE_MANIM_CODE)
        
        print(f"Created test script at {script_path}")
        
        # Create a media directory inside the temp directory
        output_dir = os.path.join(temp_dir, "output")
        os.makedirs(output_dir, exist_ok=True)
        
        # Get the path to the Python executable in the current environment
        python_executable = sys.executable
        
        # Execute Manim using the Python module approach
        cmd = [
            python_executable,
            "-m", "manim",
            "-qm",  # Medium quality
            "--output_file", "test_video",
            "--media_dir", output_dir,
            script_path,
            "CreateScene"
        ]
        
        print(f"Executing Manim command: {' '.join(cmd)}")
        
        # Run the command
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        stdout, stderr = process.communicate()
        
        # Log the output
        stdout_text = stdout.decode() if stdout else ""
        stderr_text = stderr.decode() if stderr else ""
        
        print("STDOUT:")
        print(stdout_text)
        print("\nSTDERR:")
        print(stderr_text)
        
        # Check if Manim execution was successful
        if process.returncode != 0:
            print(f"Manim execution failed with return code {process.returncode}")
            return False
        
        # Extract the output path from stdout
        output_path = extract_output_path_from_stdout(stdout_text)
        
        # Verify the video file exists if we found a path
        if output_path and os.path.exists(output_path):
            print(f"Found video file at: {output_path}")
            
            # Create a destination directory
            dest_dir = os.path.join(os.getcwd(), "test_output")
            os.makedirs(dest_dir, exist_ok=True)
            
            # Copy the video file to a permanent location
            dest_path = os.path.join(dest_dir, os.path.basename(output_path))
            shutil.copy2(output_path, dest_path)
            print(f"Copied video to: {dest_path}")
            
            print("\nTest PASSED")
            return True
        
        # If we didn't find the path in stdout, search for video files
        print("\nChecking for generated video files:")
        
        # Check various possible locations
        locations_to_check = [
            output_dir,
            os.path.join(output_dir, "videos"),
            "media",
            os.path.join("media", "videos"),
            os.getcwd(),
        ]
        
        for location in locations_to_check:
            print(f"Checking {location}...")
            if os.path.exists(location):
                video_files = find_video_files(location)
                if video_files:
                    # Create a destination directory
                    dest_dir = os.path.join(os.getcwd(), "test_output")
                    os.makedirs(dest_dir, exist_ok=True)
                    
                    # Copy the first video file to a permanent location
                    dest_path = os.path.join(dest_dir, os.path.basename(video_files[0]))
                    shutil.copy2(video_files[0], dest_path)
                    print(f"Copied video to: {dest_path}")
                    
                    print("\nTest PASSED")
                    return True
        
        print("\nNo video files found.")
        print("\nTest FAILED")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 