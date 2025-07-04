"""
Test script for audio narration functionality.
"""
import os
import asyncio
import logging
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import our services
from app.services.text_extraction import extract_narration_from_manim
from app.services.tts import text_to_speech, generate_audio_for_script, verify_api_access
from app.services.media_processing import merge_audio_video

async def test_api_access():
    """Test the Eleven Labs API access."""
    logger.info("Testing Eleven Labs API access...")
    
    success, message = await verify_api_access()
    if success:
        logger.info(f"API access test successful: {message}")
    else:
        logger.error(f"API access test failed: {message}")
        logger.error("Please check your Eleven Labs API key and internet connection.")
        logger.error("You can get an API key from: https://elevenlabs.io/app/api-key")
    
    return success

async def test_text_extraction():
    """Test the text extraction functionality."""
    logger.info("Testing text extraction...")
    
    # Sample Manim code
    manim_code = """
from manim import *

class CreateScene(Scene):
    def construct(self):
        # 1. Introduction to Calculus
        title = Text("Introduction to Calculus")
        self.play(Write(title))
        self.wait(2)
        
        # 2. Derivatives
        self.play(FadeOut(title))
        derivative_title = Text("Derivatives")
        self.play(Write(derivative_title))
        self.wait(1)
        
        # The derivative measures the rate of change
        derivative_def = Text("The derivative measures the rate of change")
        self.play(FadeOut(derivative_title))
        self.play(Write(derivative_def))
        self.wait(2)
    """
    
    # Extract narration from the Manim code
    script = extract_narration_from_manim(manim_code)
    
    # Print the extracted script
    logger.info(f"Extracted {len(script)} script segments:")
    for i, segment in enumerate(script):
        logger.info(f"  {i+1}. {segment['text']} (type: {segment['type']}, duration: {segment['timing']['duration']}s)")
    
    return script

async def test_tts():
    """Test the text-to-speech functionality."""
    logger.info("Testing text-to-speech...")
    
    # Check if Eleven Labs API key is set
    api_key = os.getenv("ELEVEN_LABS_API_KEY")
    if not api_key:
        logger.warning("ELEVEN_LABS_API_KEY not set, skipping TTS test")
        return None
    
    # Generate speech for a simple text
    test_text = "This is a test of the text-to-speech functionality."
    audio_path = await text_to_speech(test_text)
    
    if audio_path:
        logger.info(f"Generated audio saved to {audio_path}")
    else:
        logger.error("Failed to generate audio")
    
    return audio_path

async def test_audio_script_generation(script):
    """Test generating audio for a script."""
    logger.info("Testing audio script generation...")
    
    # Check if Eleven Labs API key is set
    api_key = os.getenv("ELEVEN_LABS_API_KEY")
    if not api_key:
        logger.warning("ELEVEN_LABS_API_KEY not set, skipping audio script generation test")
        return None
    
    # Generate audio for the script
    test_video_id = "test_audio_narration"
    audio_manifest = await generate_audio_for_script(script, test_video_id)
    
    if audio_manifest:
        logger.info(f"Generated audio manifest with {len(audio_manifest['segments'])} segments")
        
        # Check if there was an error
        if "error" in audio_manifest:
            logger.error(f"Error in audio manifest: {audio_manifest['error']}")
    else:
        logger.error("Failed to generate audio manifest")
    
    return audio_manifest

async def main():
    """Main test function."""
    logger.info("Starting audio narration tests...")
    
    # Test API access first
    api_success = await test_api_access()
    if not api_success:
        logger.error("API access test failed. Skipping remaining tests.")
        return
    
    # Test text extraction
    script = await test_text_extraction()
    
    # Test TTS
    audio_path = await test_tts()
    
    # Test audio script generation
    if script:
        audio_manifest = await test_audio_script_generation(script)
    
    logger.info("Audio narration tests completed!")

if __name__ == "__main__":
    asyncio.run(main()) 