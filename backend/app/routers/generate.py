"""
Router for video generation endpoints.
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
import logging
import traceback

from app.services.gemini import generate_manim_code
from app.services.manim import execute_manim_code
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

class GenerateResponse(BaseModel):
    """
    Response model for the generate endpoint.
    """
    video_id: str
    status: str

async def generate_video_task(video_id: str, prompt: str, topic: str = None, grade_level: str = None, duration_minutes: float = 3.0):
    """
    Background task for generating a video.
    
    Args:
        video_id: The ID for the video
        prompt: The prompt for generating the video
        topic: The educational topic
        grade_level: The target grade level
        duration_minutes: The desired duration in minutes
    """
    try:
        logger.info(f"Starting video generation for ID: {video_id}")
        
        # Generate Manim code using Gemini
        manim_code = await generate_manim_code(prompt, topic, grade_level, duration_minutes)
        
        # Clean the code to remove any Markdown formatting
        if "```" in manim_code:
            logger.warning("Detected Markdown code blocks in the code, cleaning...")
            manim_code = clean_code(manim_code)
        
        # Execute the Manim code to generate the video
        await execute_manim_code(video_id, manim_code)
        
        logger.info(f"Video generation completed for ID: {video_id}")
    
    except Exception as e:
        logger.error(f"Error generating video {video_id}: {str(e)}")
        logger.error(traceback.format_exc())
        # The error will be saved to an error file by the execute_manim_code function

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
            duration_minutes=request.duration_minutes
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