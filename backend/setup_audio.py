"""
Setup script for audio narration feature.
"""
import os
import asyncio
import logging
from pathlib import Path
from dotenv import load_dotenv, set_key

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def setup_audio_narration():
    """
    Set up the audio narration feature.
    """
    print("\n===== Audio Narration Setup =====\n")
    
    # Check if .env file exists
    env_file = Path("./.env")
    if not env_file.exists():
        logger.info("Creating new .env file")
        with open(env_file, "w") as f:
            f.write("# EduTutor Environment Variables\n\n")
    
    # Load environment variables
    load_dotenv()
    
    # Check if ELEVEN_LABS_API_KEY is already set
    eleven_labs_api_key = os.getenv("ELEVEN_LABS_API_KEY")
    if eleven_labs_api_key:
        print("Eleven Labs API key is already set.")
        print("Do you want to update it? (y/n)")
        update = input("> ").strip().lower()
        if update != "y":
            print("Keeping the existing API key.")
            return
    
    # Prompt for Eleven Labs API key
    print("\nTo use the audio narration feature, you need an Eleven Labs API key.")
    print("You can get one from: https://elevenlabs.io/app/api-key")
    print("\nPlease enter your Eleven Labs API key:")
    api_key = input("> ").strip()
    
    if not api_key:
        logger.warning("No API key provided. Audio narration will not be available.")
        return
    
    # Update the .env file
    set_key(env_file, "ELEVEN_LABS_API_KEY", api_key)
    logger.info("Eleven Labs API key has been set in .env file")
    
    # Also set the environment variable for the current session
    os.environ["ELEVEN_LABS_API_KEY"] = api_key
    
    # Test the API key
    print("\nTesting the API key...")
    from app.services.tts import verify_api_access
    
    success, message = await verify_api_access()
    if success:
        print(f"✅ API key is valid: {message}")
        print("\nYou're all set! Audio narration is now available.")
    else:
        print(f"❌ API key test failed: {message}")
        print("\nPlease check your API key and try again.")

if __name__ == "__main__":
    asyncio.run(setup_audio_narration()) 