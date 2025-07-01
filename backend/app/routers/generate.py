"""
Video generation endpoints for EduTutor.
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional

from app.services.gemini import generate_manim_code
from app.services.manim import execute_manim_code
from app.utils.helpers import generate_unique_id

router = APIRouter()

class GenerateRequest(BaseModel):
    """Request model for video generation."""
    prompt: str
    complexity: Optional[str] = "medium"  # simple, medium, complex
    duration: Optional[int] = 60  # target duration in seconds

class GenerateResponse(BaseModel):
    """Response model for video generation."""
    video_id: str
    status: str
    message: str

@router.post("/generate", response_model=GenerateResponse)
async def generate_video(request: GenerateRequest, background_tasks: BackgroundTasks):
    """
    Generate an educational video based on the provided prompt.
    
    Args:
        request: The generation request containing the prompt and options
        background_tasks: FastAPI background tasks for async processing
        
    Returns:
        Response with video ID and status
    """
    try:
        # Generate a unique ID for this video
        video_id = generate_unique_id()
        
        # Generate Manim code using Gemini
        manim_code = await generate_manim_code(request.prompt, request.complexity, request.duration)
        
        # Execute Manim code in the background
        background_tasks.add_task(
            execute_manim_code,
            video_id=video_id,
            manim_code=manim_code
        )
        
        return GenerateResponse(
            video_id=video_id,
            status="processing",
            message="Video generation started. Check the status endpoint for updates."
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Video generation failed: {str(e)}")

@router.get("/video/{video_id}", response_model=dict)
async def get_video_status(video_id: str):
    """
    Get the status of a video generation request.
    
    Args:
        video_id: The unique ID of the video
        
    Returns:
        Status information about the video generation process
    """
    # TODO: Implement status checking from storage
    # This would check if the video exists and its processing status
    
    # Placeholder implementation
    return {
        "video_id": video_id,
        "status": "processing",  # processing, completed, failed
        "message": "Video is being generated",
        "url": None  # Will be populated when video is ready
    } 