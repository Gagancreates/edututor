"""
Router for video generation endpoints.
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
import logging
import traceback
import os
import json

from app.services.gemini import generate_manim_code
from app.services.manim import execute_manim_code
from app.services.elevenlabs import NarrationManager
from app.services.audio import AudioProcessor
from app.utils.helpers import generate_uuid, clean_code, get_video_status

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["generate"])

class GenerateRequest(BaseModel):
    """
    Request model for generating a video.
    """
    prompt: str
    topic: str = None
    grade_level: str = None
    duration_minutes: float = 3.0
    enable_narration: bool = False
    voice_id: str = None  # Optional voice ID for narration

class GenerateResponse(BaseModel):
    """
    Response model for the generate endpoint.
    """
    video_id: str
    status: str

class VoiceInfo(BaseModel):
    """
    Model for voice information.
    """
    voice_id: str
    name: str
    description: str = None
    preview_url: str = None
    category: str = None

class VoicesResponse(BaseModel):
    """
    Response model for the list voices endpoint.
    """
    voices: list[VoiceInfo]

async def generate_video_task(
    video_id: str, 
    prompt: str, 
    topic: str = None, 
    grade_level: str = None, 
    duration_minutes: float = 3.0,
    enable_narration: bool = False,
    voice_id: str = None
):
    """
    Background task for generating a video.
    
    Args:
        video_id: The ID for the video
        prompt: The prompt for generating the video
        topic: The educational topic
        grade_level: The target grade level
        duration_minutes: The desired duration in minutes
        enable_narration: Whether to enable voice narration
        voice_id: The ID of the voice to use for narration
    """
    try:
        logger.info(f"Starting video generation for ID: {video_id}")
        
        # Create videos directory for this video_id if it doesn't exist
        video_dir = os.path.join("videos", video_id)
        os.makedirs(video_dir, exist_ok=True)
        
        # Generate Manim code using Gemini with timeout handling
        try:
            manim_code = await generate_manim_code(
                prompt=prompt, 
                topic=topic, 
                grade_level=grade_level, 
                duration_minutes=duration_minutes,
                max_retries=3,
                timeout=180.0  # 3 minutes timeout
            )
        except Exception as e:
            logger.error(f"Error generating Manim code: {str(e)}")
            
            # Save detailed error information
            error_file = os.path.join(video_dir, "error.txt")
            with open(error_file, "w") as f:
                error_message = f"Failed to generate Manim code: {str(e)}\n\n"
                error_message += "This might be due to:\n"
                error_message += "- The prompt being too complex or broad\n"
                error_message += "- The Gemini API experiencing high traffic\n\n"
                error_message += "Please try:\n"
                error_message += "- Using a more specific and focused prompt\n"
                error_message += "- Breaking down complex topics into smaller parts\n"
                error_message += "- Trying again in a few minutes\n\n"
                error_message += traceback.format_exc()
                f.write(error_message)
            
            # Save metadata for frontend to display
            metadata_file = os.path.join(video_dir, "metadata.json")
            with open(metadata_file, "w") as f:
                metadata = {
                    "status": "error",
                    "error_type": "generation_failed",
                    "prompt": prompt,
                    "topic": topic,
                    "message": f"Failed to generate code: {str(e)}"
                }
                json.dump(metadata, f)
            
            logger.error(f"Generation failed for video {video_id}. Error saved to {error_file}")
            return
        
        # Clean the code to remove any Markdown formatting
        if "```" in manim_code:
            logger.warning("Detected Markdown code blocks in the code, cleaning...")
            manim_code = clean_code(manim_code)
        
        # Save the generated code
        code_file = os.path.join(video_dir, f"{video_id}.py")
        with open(code_file, "w") as f:
            f.write(manim_code)
        
        # Execute the Manim code to generate the video
        video_path = await execute_manim_code(video_id, manim_code)
        
        # Generate narration if enabled
        if enable_narration and video_path:
            try:
                logger.info(f"Generating narration for video {video_id}")
                
                # Initialize the narration manager
                narration_manager = NarrationManager()
                
                # Generate narration audio
                narration_result = await narration_manager.generate_full_narration(
                    manim_code=manim_code,
                    output_dir=video_dir,
                    voice_id=voice_id
                )
                
                if narration_result["success"]:
                    logger.info(f"Narration generated successfully for video {video_id}")
                    
                    # Get the paths
                    audio_path = narration_result["audio_path"]
                    
                    # Merge audio and video
                    audio_processor = AudioProcessor()
                    output_path = os.path.join(video_dir, f"{video_id}_narrated.mp4")
                    
                    # Synchronize and merge
                    final_video = await audio_processor.sync_audio_to_video(
                        video_path=video_path,
                        audio_path=audio_path,
                        output_path=output_path
                    )
                    
                    if final_video:
                        logger.info(f"Audio and video merged successfully for {video_id}")
                        
                        # Save metadata about narration
                        metadata_file = os.path.join(video_dir, "metadata.json")
                        with open(metadata_file, "w") as f:
                            metadata = {
                                "status": "completed",
                                "has_narration": True,
                                "prompt": prompt,
                                "topic": topic,
                                "voice_id": voice_id,
                                "original_video": os.path.basename(video_path),
                                "narrated_video": os.path.basename(final_video)
                            }
                            json.dump(metadata, f)
                    else:
                        logger.error(f"Failed to merge audio and video for {video_id}")
                else:
                    logger.error(f"Failed to generate narration: {narration_result.get('error', 'Unknown error')}")
            except Exception as e:
                logger.error(f"Error in narration process: {str(e)}")
                logger.error(traceback.format_exc())
                # Continue without narration if it fails
        
        logger.info(f"Video generation completed for ID: {video_id}")
    
    except Exception as e:
        logger.error(f"Error generating video {video_id}: {str(e)}")
        logger.error(traceback.format_exc())
        
        # Ensure the video directory exists
        video_dir = os.path.join("videos", video_id)
        os.makedirs(video_dir, exist_ok=True)
        
        # Save the error to a file
        error_file = os.path.join(video_dir, "error.txt")
        with open(error_file, "w") as f:
            f.write(f"Error: {str(e)}\n\n{traceback.format_exc()}")

@router.post("/generate", response_model=GenerateResponse)
async def generate_video(request: GenerateRequest, background_tasks: BackgroundTasks):
    """
    Generate an educational video using Manim based on the provided prompt.
    
    Args:
        request: The request containing the prompt and other parameters
        background_tasks: FastAPI background tasks
        
    Returns:
        Response with the video ID and status
    """
    try:
        # Generate a unique ID for the video
        video_id = generate_uuid()
        
        # Start the video generation in the background
        background_tasks.add_task(
            generate_video_task,
            video_id=video_id,
            prompt=request.prompt,
            topic=request.topic,
            grade_level=request.grade_level,
            duration_minutes=request.duration_minutes,
            enable_narration=request.enable_narration,
            voice_id=request.voice_id
        )
        
        return GenerateResponse(
            video_id=video_id,
            status="processing"
        )
    
    except Exception as e:
        logger.error(f"Error initiating video generation: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Failed to initiate video generation: {str(e)}")

@router.get("/video/{video_id}/status", response_model=dict)
async def get_video_status_endpoint(video_id: str):
    """
    Get the status of a video generation process.
    
    Args:
        video_id: The ID of the video
        
    Returns:
        Status information for the video
    """
    try:
        logger.info(f"Checking status for video ID: {video_id}")
        status = get_video_status(video_id)
        return status
    
    except Exception as e:
        logger.error(f"Error checking video status for {video_id}: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error checking video status: {str(e)}")

@router.get("/voices", response_model=VoicesResponse)
async def list_voices():
    """
    List available voices for narration.
    
    Returns:
        List of available voices
    """
    try:
        narration_manager = NarrationManager()
        voices = await narration_manager.list_available_voices()
        
        return VoicesResponse(voices=voices)
    
    except Exception as e:
        logger.error(f"Error listing voices: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error listing voices: {str(e)}") 