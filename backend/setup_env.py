"""
Environment setup script for EduTutor backend.
"""
import os
import sys
from pathlib import Path
import logging
from dotenv import load_dotenv, set_key

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_environment():
    """
    Set up environment variables for the application.
    """
    # Load existing environment variables
    load_dotenv()
    
    # Check if .env file exists, if not create it
    env_file = ".env"
    if not os.path.exists(env_file):
        with open(env_file, "w") as f:
            f.write("# Environment variables for the application\n")
    
    # Set up Gemini API key
    gemini_api_key = os.environ.get("GEMINI_API_KEY")
    if not gemini_api_key:
        logger.info("GEMINI_API_KEY not found in environment variables")
        gemini_api_key = input("Enter your Gemini API key: ")
        if gemini_api_key:
            set_key(env_file, "GEMINI_API_KEY", gemini_api_key)
            logger.info("GEMINI_API_KEY set successfully")
        else:
            logger.warning("GEMINI_API_KEY not set")
    else:
        logger.info("GEMINI_API_KEY already set")
    
    # Set up ElevenLabs API key
    elevenlabs_api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not elevenlabs_api_key:
        logger.info("ELEVENLABS_API_KEY not found in environment variables")
        elevenlabs_api_key = input("Enter your ElevenLabs API key (press Enter to skip): ")
        if elevenlabs_api_key:
            set_key(env_file, "ELEVENLABS_API_KEY", elevenlabs_api_key)
            logger.info("ELEVENLABS_API_KEY set successfully")
        else:
            logger.warning("ELEVENLABS_API_KEY not set, voice narration will be disabled")
    else:
        logger.info("ELEVENLABS_API_KEY already set")
    
    logger.info("Environment setup complete")

if __name__ == "__main__":
    setup_environment()
    print("\nEnvironment setup complete!")
    print("You can now run the application.") 