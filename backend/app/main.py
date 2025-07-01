"""
Main FastAPI application module.
"""
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
import os
import logging
from pathlib import Path
import traceback

from app.routers import generate
from app.utils.helpers import get_video_path, generate_uuid

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="EduTutor API", version="0.1.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(generate.router)

@app.get("/")
async def root():
    """
    Root endpoint for the API.
    """
    return {"message": "Welcome to EduTutor API"}

@app.get("/api/health")
async def health_check():
    """
    Health check endpoint.
    """
    return {"status": "healthy"}

@app.get("/api/video/{video_id}")
async def get_video(video_id: str):
    """
    Get a generated video by ID.
    
    Args:
        video_id: The ID of the video
        
    Returns:
        The video file or an error message
    """
    try:
        logger.info(f"Fetching video with ID: {video_id}")
        
        # Get the path to the video file
        video_path = get_video_path(video_id)
        
        if not video_path:
            # Check if there's an error file
            error_path = Path(f"./videos/{video_id}/error.txt")
            if error_path.exists():
                with open(error_path, "r") as f:
                    error_message = f.read()
                logger.error(f"Error for video {video_id}: {error_message}")
                raise HTTPException(status_code=500, detail=f"Video generation failed: {error_message}")
            
            logger.error(f"Video with ID {video_id} not found")
            raise HTTPException(status_code=404, detail=f"Video with ID {video_id} not found")
        
        logger.info(f"Returning video from path: {video_path}")
        return FileResponse(
            path=video_path,
            media_type="video/mp4",
            filename=f"{video_id}.mp4"
        )
    
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    
    except Exception as e:
        logger.error(f"Error fetching video {video_id}: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error fetching video: {str(e)}")

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Global exception handler for the application.
    """
    logger.error(f"Unhandled exception: {str(exc)}")
    logger.error(traceback.format_exc())
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 