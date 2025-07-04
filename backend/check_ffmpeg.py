"""
Script to check if FFmpeg is installed and accessible.
"""
import subprocess
import sys
import os
import platform
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def check_ffmpeg():
    """Check if FFmpeg is installed and accessible."""
    try:
        # Run ffmpeg -version command
        result = subprocess.run(
            ["ffmpeg", "-version"],
            capture_output=True,
            text=True,
            check=False
        )
        
        if result.returncode == 0:
            version_info = result.stdout.split("\n")[0]
            logger.info(f"FFmpeg is installed: {version_info}")
            return True, version_info
        else:
            logger.error(f"FFmpeg check failed with return code {result.returncode}")
            logger.error(f"Error output: {result.stderr}")
            return False, result.stderr
    
    except FileNotFoundError:
        logger.error("FFmpeg not found. Please install FFmpeg and make sure it's in your PATH.")
        return False, "FFmpeg not found in PATH"
    
    except Exception as e:
        logger.error(f"Error checking FFmpeg: {str(e)}")
        return False, str(e)

def check_ffmpeg_capabilities():
    """Check FFmpeg capabilities for audio-video processing."""
    try:
        # Check if FFmpeg supports the codecs and formats we need
        result = subprocess.run(
            ["ffmpeg", "-codecs"],
            capture_output=True,
            text=True,
            check=False
        )
        
        if result.returncode != 0:
            logger.error(f"Failed to check FFmpeg codecs: {result.stderr}")
            return False
        
        codecs_output = result.stdout.lower()
        
        # Check for required codecs
        required_codecs = ["aac", "mp3", "h264"]
        missing_codecs = []
        
        for codec in required_codecs:
            if codec not in codecs_output:
                missing_codecs.append(codec)
        
        if missing_codecs:
            logger.warning(f"Missing required codecs: {', '.join(missing_codecs)}")
        else:
            logger.info("All required codecs are supported")
        
        # Check for concat demuxer
        result = subprocess.run(
            ["ffmpeg", "-formats"],
            capture_output=True,
            text=True,
            check=False
        )
        
        if result.returncode != 0:
            logger.error(f"Failed to check FFmpeg formats: {result.stderr}")
            return False
        
        formats_output = result.stdout.lower()
        
        if "concat" not in formats_output:
            logger.warning("FFmpeg concat demuxer not found")
            return False
        
        logger.info("FFmpeg concat demuxer is supported")
        return True
    
    except Exception as e:
        logger.error(f"Error checking FFmpeg capabilities: {str(e)}")
        return False

def test_basic_ffmpeg_operation():
    """Test a basic FFmpeg operation to verify functionality."""
    try:
        # Create a test directory
        os.makedirs("temp", exist_ok=True)
        test_file = os.path.join("temp", "ffmpeg_test.txt")
        
        # Create a test file with some content
        with open(test_file, "w") as f:
            f.write("FFmpeg test file")
        
        # Run a simple FFmpeg command (just to test if it runs)
        result = subprocess.run(
            ["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono", "-t", "1", 
             os.path.join("temp", "test_audio.mp3")],
            capture_output=True,
            text=True,
            check=False
        )
        
        if result.returncode == 0:
            logger.info("Basic FFmpeg operation successful")
            return True
        else:
            logger.error(f"Basic FFmpeg operation failed: {result.stderr}")
            return False
    
    except Exception as e:
        logger.error(f"Error testing basic FFmpeg operation: {str(e)}")
        return False

def get_system_info():
    """Get system information."""
    system_info = {
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "architecture": platform.architecture(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "python_version": sys.version,
        "cwd": os.getcwd(),
        "path": os.environ.get("PATH", "")
    }
    
    return system_info

def main():
    """Main function."""
    logger.info("Checking FFmpeg installation and capabilities...")
    
    # Get system information
    system_info = get_system_info()
    logger.info(f"System: {system_info['system']} {system_info['release']} {system_info['version']}")
    logger.info(f"Architecture: {system_info['architecture']}")
    logger.info(f"Python version: {system_info['python_version'].split()[0]}")
    
    # Check if FFmpeg is installed
    ffmpeg_installed, version_info = check_ffmpeg()
    
    if not ffmpeg_installed:
        logger.error("FFmpeg check failed. Please install FFmpeg and make sure it's in your PATH.")
        sys.exit(1)
    
    # Check FFmpeg capabilities
    capabilities_ok = check_ffmpeg_capabilities()
    
    if not capabilities_ok:
        logger.warning("FFmpeg may not have all required capabilities.")
    
    # Test basic FFmpeg operation
    operation_ok = test_basic_ffmpeg_operation()
    
    if not operation_ok:
        logger.error("Basic FFmpeg operation failed.")
        sys.exit(1)
    
    logger.info("FFmpeg checks completed successfully.")

if __name__ == "__main__":
    main() 