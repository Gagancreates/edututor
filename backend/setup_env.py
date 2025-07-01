"""
Environment setup script for EduTutor backend.
"""
import os
import sys
from pathlib import Path
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_environment():
    """
    Set up environment variables for the application.
    """
    # Check if .env file exists
    env_file = Path("./.env")
    if not env_file.exists():
        # Create a new .env file
        logger.info("Creating new .env file")
        with open(env_file, "w") as f:
            f.write("# EduTutor Environment Variables\n\n")
            f.write("# Google Gemini API Key\n")
            f.write("GEMINI_API_KEY=\n")
    
    # Check if GEMINI_API_KEY is set
    with open(env_file, "r") as f:
        env_content = f.read()
    
    if "GEMINI_API_KEY=" in env_content and "GEMINI_API_KEY=your_api_key_here" not in env_content:
        # Check if the key is already set
        key_line = [line for line in env_content.splitlines() if line.startswith("GEMINI_API_KEY=")][0]
        if len(key_line) > 14:  # "GEMINI_API_KEY=" is 14 characters
            logger.info("GEMINI_API_KEY is already set in .env file")
            return
    
    # Prompt for API key
    print("\n===== EduTutor Environment Setup =====")
    print("\nTo use the Gemini API, you need to provide an API key.")
    print("You can get one from: https://aistudio.google.com/app/apikey")
    print("\nPlease enter your Gemini API key:")
    api_key = input("> ").strip()
    
    if not api_key:
        logger.warning("No API key provided. The application may not function correctly.")
        return
    
    # Update the .env file
    if "GEMINI_API_KEY=" in env_content:
        # Replace the existing line
        new_content = []
        for line in env_content.splitlines():
            if line.startswith("GEMINI_API_KEY="):
                new_content.append(f"GEMINI_API_KEY={api_key}")
            else:
                new_content.append(line)
        
        with open(env_file, "w") as f:
            f.write("\n".join(new_content))
    else:
        # Append to the file
        with open(env_file, "a") as f:
            f.write(f"\n# Google Gemini API Key\nGEMINI_API_KEY={api_key}\n")
    
    logger.info("GEMINI_API_KEY has been set in .env file")
    
    # Also set the environment variable for the current session
    os.environ["GEMINI_API_KEY"] = api_key
    logger.info("GEMINI_API_KEY has been set in the current environment")

if __name__ == "__main__":
    setup_environment()
    print("\nEnvironment setup complete!")
    print("You can now run the application.") 