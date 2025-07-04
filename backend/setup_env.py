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
            f.write("\n# Eleven Labs API Key\n")
            f.write("ELEVEN_LABS_API_KEY=\n")
    
    # Read the current .env file
    with open(env_file, "r") as f:
        env_content = f.read()
    
    # Check if GEMINI_API_KEY is set
    gemini_key_set = False
    if "GEMINI_API_KEY=" in env_content and "GEMINI_API_KEY=your_api_key_here" not in env_content:
        # Check if the key is already set
        key_line = [line for line in env_content.splitlines() if line.startswith("GEMINI_API_KEY=")][0]
        if len(key_line) > 14:  # "GEMINI_API_KEY=" is 14 characters
            logger.info("GEMINI_API_KEY is already set in .env file")
            gemini_key_set = True
    
    # Check if ELEVEN_LABS_API_KEY is set
    eleven_labs_key_set = False
    if "ELEVEN_LABS_API_KEY=" in env_content and "ELEVEN_LABS_API_KEY=your_api_key_here" not in env_content:
        # Check if the key is already set
        key_line = [line for line in env_content.splitlines() if line.startswith("ELEVEN_LABS_API_KEY=")][0]
        if len(key_line) > 19:  # "ELEVEN_LABS_API_KEY=" is 19 characters
            logger.info("ELEVEN_LABS_API_KEY is already set in .env file")
            eleven_labs_key_set = True
    
    # Prompt for API keys if needed
    print("\n===== EduTutor Environment Setup =====")
    
    # Gemini API key
    gemini_api_key = None
    if not gemini_key_set:
        print("\nTo use the Gemini API, you need to provide an API key.")
        print("You can get one from: https://aistudio.google.com/app/apikey")
        print("\nPlease enter your Gemini API key:")
        gemini_api_key = input("> ").strip()
        
        if not gemini_api_key:
            logger.warning("No Gemini API key provided. The application may not function correctly.")
    
    # Eleven Labs API key
    eleven_labs_api_key = None
    if not eleven_labs_key_set:
        print("\nTo use the Eleven Labs API for text-to-speech, you need to provide an API key.")
        print("You can get one from: https://elevenlabs.io/app/api-key")
        print("\nPlease enter your Eleven Labs API key (or press Enter to skip):")
        eleven_labs_api_key = input("> ").strip()
        
        if not eleven_labs_api_key:
            logger.warning("No Eleven Labs API key provided. Audio narration will not be available.")
    
    # Update the .env file with the Gemini API key
    if gemini_api_key:
        if "GEMINI_API_KEY=" in env_content:
            # Replace the existing line
            new_content = []
            for line in env_content.splitlines():
                if line.startswith("GEMINI_API_KEY="):
                    new_content.append(f"GEMINI_API_KEY={gemini_api_key}")
                else:
                    new_content.append(line)
            
            env_content = "\n".join(new_content)
        else:
            # Append to the file
            env_content += f"\n# Google Gemini API Key\nGEMINI_API_KEY={gemini_api_key}\n"
        
        logger.info("GEMINI_API_KEY has been set in .env file")
        
        # Also set the environment variable for the current session
        os.environ["GEMINI_API_KEY"] = gemini_api_key
        logger.info("GEMINI_API_KEY has been set in the current environment")
    
    # Update the .env file with the Eleven Labs API key
    if eleven_labs_api_key:
        if "ELEVEN_LABS_API_KEY=" in env_content:
            # Replace the existing line
            new_content = []
            for line in env_content.splitlines():
                if line.startswith("ELEVEN_LABS_API_KEY="):
                    new_content.append(f"ELEVEN_LABS_API_KEY={eleven_labs_api_key}")
                else:
                    new_content.append(line)
            
            env_content = "\n".join(new_content)
        else:
            # Append to the file
            env_content += f"\n# Eleven Labs API Key\nELEVEN_LABS_API_KEY={eleven_labs_api_key}\n"
        
        logger.info("ELEVEN_LABS_API_KEY has been set in .env file")
        
        # Also set the environment variable for the current session
        os.environ["ELEVEN_LABS_API_KEY"] = eleven_labs_api_key
        logger.info("ELEVEN_LABS_API_KEY has been set in the current environment")
    
    # Write the updated content back to the .env file
    with open(env_file, "w") as f:
        f.write(env_content)

if __name__ == "__main__":
    setup_environment()
    print("\nEnvironment setup complete!")
    print("You can now run the application.") 