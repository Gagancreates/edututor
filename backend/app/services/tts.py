"""
Text-to-speech service using Eleven Labs API.
"""
import os
import logging
import asyncio
import json
import requests
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple
from elevenlabs import generate, save, set_api_key, Voice, voices
from elevenlabs.api import Models

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load API key from environment variables
ELEVEN_LABS_API_KEY = os.getenv("ELEVEN_LABS_API_KEY")
if ELEVEN_LABS_API_KEY:
    set_api_key(ELEVEN_LABS_API_KEY)
else:
    logger.warning("ELEVEN_LABS_API_KEY not found in environment variables")

# Define the directory for storing generated audio
AUDIO_DIR = Path("./audio")
os.makedirs(AUDIO_DIR, exist_ok=True)

# Default voice ID for educational content
DEFAULT_VOICE_ID = "EXAVITQu4vr4xnSDxMaL"  # Adam voice (clear, professional)

# Cache available voices
_available_voices = None

async def verify_api_access() -> Tuple[bool, str]:
    """
    Verify that the Eleven Labs API is accessible and the API key is valid.
    
    Returns:
        Tuple of (success, message)
    """
    if not ELEVEN_LABS_API_KEY:
        return False, "ELEVEN_LABS_API_KEY not set"
    
    try:
        # Make a simple API request to check access
        response = requests.get(
            "https://api.elevenlabs.io/v1/voices",
            headers={"xi-api-key": ELEVEN_LABS_API_KEY}
        )
        
        if response.status_code == 200:
            voice_count = len(response.json().get("voices", []))
            return True, f"API access verified. {voice_count} voices available."
        elif response.status_code == 401:
            return False, "Authentication failed. Invalid API key."
        elif response.status_code == 403:
            return False, "Access forbidden. Check API key permissions."
        else:
            return False, f"API request failed with status code {response.status_code}: {response.text}"
    
    except Exception as e:
        return False, f"Error verifying API access: {str(e)}"

async def get_available_voices() -> List[Voice]:
    """
    Get available voices from Eleven Labs API.
    
    Returns:
        List of available voices
    """
    global _available_voices
    
    if _available_voices is None:
        try:
            _available_voices = voices()
            logger.info(f"Retrieved {len(_available_voices)} voices from Eleven Labs API")
        except Exception as e:
            logger.error(f"Error retrieving voices from Eleven Labs API: {str(e)}")
            _available_voices = []
    
    return _available_voices

async def text_to_speech(
    text: str,
    voice_id: str = DEFAULT_VOICE_ID,
    output_path: Optional[Path] = None,
    model_id: str = "eleven_monolingual_v1"
) -> Optional[Path]:
    """
    Convert text to speech using Eleven Labs API.
    
    Args:
        text: The text to convert to speech
        voice_id: The ID of the voice to use
        output_path: The path to save the audio file (if None, a path will be generated)
        model_id: The ID of the TTS model to use
        
    Returns:
        Path to the generated audio file or None if generation failed
    """
    if not ELEVEN_LABS_API_KEY:
        logger.error("Cannot generate audio: ELEVEN_LABS_API_KEY not set")
        return None
    
    # Generate output path if not provided
    if output_path is None:
        # Create a hash of the text to use as filename
        import hashlib
        text_hash = hashlib.md5(text.encode()).hexdigest()[:16]
        output_path = AUDIO_DIR / f"{text_hash}.mp3"
    
    # Create parent directory if it doesn't exist
    os.makedirs(output_path.parent, exist_ok=True)
    
    try:
        logger.info(f"Generating speech for text: '{text[:50]}...' with voice {voice_id}")
        
        # Run in a separate thread to avoid blocking
        audio = await asyncio.to_thread(
            generate,
            text=text,
            voice=voice_id,
            model=model_id
        )
        
        # Save the audio to the output path
        await asyncio.to_thread(save, audio, str(output_path))
        
        logger.info(f"Speech generated and saved to {output_path}")
        return output_path
    
    except Exception as e:
        # Provide more detailed error message
        error_type = type(e).__name__
        error_msg = str(e)
        
        if "401" in error_msg:
            logger.error(f"Error generating speech: Authentication failed. Check your Eleven Labs API key. ({error_type}: {error_msg})")
        elif "403" in error_msg:
            logger.error(f"Error generating speech: Access forbidden. Your API key may not have permission. ({error_type}: {error_msg})")
        elif "429" in error_msg:
            logger.error(f"Error generating speech: Rate limit exceeded. ({error_type}: {error_msg})")
        elif "voice" in error_msg.lower():
            logger.error(f"Error generating speech: Voice ID issue. The voice ID '{voice_id}' may not exist. ({error_type}: {error_msg})")
        else:
            logger.error(f"Error generating speech: {error_type}: {error_msg}")
        
        return None

async def generate_audio_for_script(
    script: List[Dict[str, Any]],
    video_id: str,
    voice_id: str = DEFAULT_VOICE_ID
) -> Dict[str, Any]:
    """
    Generate audio for a script with multiple segments.
    
    Args:
        script: List of script segments with 'text' and 'timing' keys
        video_id: The ID of the video
        voice_id: The ID of the voice to use
        
    Returns:
        Dictionary with paths to generated audio files and metadata
    """
    # First verify API access
    api_success, api_message = await verify_api_access()
    if not api_success:
        logger.error(f"Cannot generate audio for script: {api_message}")
        return {"video_id": video_id, "voice_id": voice_id, "segments": [], "error": api_message}
    
    # Create directory for this video's audio files
    video_audio_dir = AUDIO_DIR / video_id
    os.makedirs(video_audio_dir, exist_ok=True)
    
    # Save the script for reference
    script_path = video_audio_dir / "script.json"
    with open(script_path, "w") as f:
        json.dump(script, f, indent=2)
    
    # Generate audio for each segment
    audio_segments = []
    for i, segment in enumerate(script):
        segment_text = segment["text"]
        segment_timing = segment.get("timing", {})
        
        # Skip empty segments
        if not segment_text.strip():
            continue
        
        # Generate output path for this segment
        segment_path = video_audio_dir / f"segment_{i:03d}.mp3"
        
        # Generate audio for this segment
        audio_path = await text_to_speech(
            text=segment_text,
            voice_id=voice_id,
            output_path=segment_path
        )
        
        if audio_path:
            audio_segments.append({
                "index": i,
                "text": segment_text,
                "timing": segment_timing,
                "audio_path": str(audio_path)
            })
    
    # Create a manifest file with all audio segments
    manifest = {
        "video_id": video_id,
        "voice_id": voice_id,
        "segments": audio_segments
    }
    
    manifest_path = video_audio_dir / "manifest.json"
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)
    
    return manifest 