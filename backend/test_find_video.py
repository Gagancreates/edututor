"""
Test script to find and copy video files from Manim output.
"""
import os
import sys
import tempfile
import subprocess
import shutil
import glob
from pathlib import Path

def find_video_files(directory):
    """Find all video files in a directory and its subdirectories"""
    video_files = []
    
    # Use glob to find all MP4 files recursively
    video_files = list(Path(directory).glob("**/*.mp4"))
    
    print(f"Found {len(video_files)} video files in {directory}")
    for video_file in video_files:
        print(f"  - {video_file}")
    
    return video_files

def main():
    """Main test function"""
    print("Testing video file search and copy...")
    
    # Create a simple Manim script
    manim_code = """
from manim import *

class CreateScene(Scene):
    def construct(self):
        # Create a circle
        circle = Circle(color=BLUE)
        self.play(Create(circle))
        
        # Add text
        text = Text("Testing Video File Search")
        self.play(Write(text))
        
        # Fade out
        self.play(FadeOut(circle), FadeOut(text))
"""
    
    # Create a temporary directory for the test
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"Created temporary directory at {temp_dir}")
        
        # Create a Python file with the Manim code
        script_path = os.path.join(temp_dir, "test_video.py")
        with open(script_path, "w") as f:
            f.write(manim_code)
        
        # Create an output directory
        output_dir = os.path.join(temp_dir, "output")
        os.makedirs(output_dir, exist_ok=True)
        
        # Get the path to the Python executable
        python_executable = sys.executable
        
        # Execute Manim
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
        
        print("\nSTDOUT:")
        print(stdout_text)
        
        print("\nSTDERR:")
        print(stderr_text)
        
        # Extract the output path from stdout
        output_path = None
        for line in stdout_text.splitlines():
            if "File ready at" in line:
                path_start = line.find("'")
                if path_start != -1:
                    path_end = line.find("'", path_start + 1)
                    if path_end != -1:
                        output_path = line[path_start + 1:path_end]
                        print(f"\nExtracted output path from stdout: {output_path}")
                        break
        
        # Check if the output path exists
        if output_path and os.path.exists(output_path):
            print(f"Output path exists: {output_path}")
        else:
            print(f"Output path does not exist or was not found")
        
        # Search for video files in the output directory
        print("\nSearching for video files in the output directory:")
        video_files = find_video_files(output_dir)
        
        # Check the expected Manim output structure
        expected_path = os.path.join(output_dir, "videos", "test_video", "720p30")
        if os.path.exists(expected_path):
            print(f"\nExpected path exists: {expected_path}")
            expected_files = find_video_files(expected_path)
        else:
            print(f"\nExpected path does not exist: {expected_path}")
        
        # Try to find videos using glob directly
        print("\nSearching for video files using glob:")
        glob_files = glob.glob(os.path.join(output_dir, "**", "*.mp4"), recursive=True)
        for file in glob_files:
            print(f"  - {file}")
        
        # If we found video files, copy the first one to a permanent location
        if video_files:
            dest_dir = os.path.join(os.getcwd(), "test_output")
            os.makedirs(dest_dir, exist_ok=True)
            
            video_file = video_files[0]
            dest_path = os.path.join(dest_dir, os.path.basename(str(video_file)))
            
            print(f"\nCopying {video_file} to {dest_path}")
            shutil.copy2(video_file, dest_path)
            
            print("\nTest PASSED - Video file found and copied")
            return True
        else:
            print("\nTest FAILED - No video files found")
            return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 