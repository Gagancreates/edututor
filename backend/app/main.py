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
from app.utils.helpers import get_video_path, generate_uuid, is_audio_processing

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
# Set debug level for media processing module
logging.getLogger("app.services.media_processing").setLevel(logging.DEBUG)

app = FastAPI(title="EduTutor API", version="0.1.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
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
    Get a video by ID.
    """
    try:
        app.logger.info(f"Fetching video with ID: {video_id}")
        
        # Check if audio processing is in progress
        if is_audio_processing(video_id):
            app.logger.info(f"Audio processing in progress for video {video_id}")
            return JSONResponse(
                content={
                    "video_id": video_id,
                    "status": "processing",
                    "message": "Adding audio narration to video"
                },
                status_code=202  # Accepted but still processing
            )
        
        # Get the path to the video file
        video_path = get_video_path(video_id)
        
        if not video_path:
            # Check if there's an error file
            error_path = Path(f"videos/{video_id}/error.txt")
            if error_path.exists():
                with open(error_path, "r") as f:
                    error_message = f.read()
                app.logger.error(f"Error for video {video_id}: {error_message}")
                raise HTTPException(status_code=500, detail=f"Video generation failed: {error_message}")
            
            # Check if the directory exists but video is still processing
            video_dir = Path(f"videos/{video_id}")
            if video_dir.exists():
                app.logger.info(f"Video {video_id} is still processing")
                return JSONResponse(
                    content={
                        "video_id": video_id,
                        "status": "processing",
                        "message": "Video generation in progress"
                    },
                    status_code=202  # Accepted but still processing
                )
            
            app.logger.error(f"Video with ID {video_id} not found")
            raise HTTPException(status_code=404, detail=f"Video with ID {video_id} not found")
        
        # Check if this is a narrated video
        is_narrated = "_with_audio" in video_path
        
        app.logger.info(f"Returning video from path: {video_path} (narrated: {is_narrated})")
        return FileResponse(
            path=video_path,
            media_type="video/mp4",
            filename=f"{video_id}.mp4"
        )
    
    except Exception as e:
        app.logger.error(f"Error fetching video {video_id}: {str(e)}")
        app.logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error fetching video: {str(e)}")

@app.get("/api/video/{video_id}/status")
async def get_video_status_direct(video_id: str):
    """
    Get the status of a video directly.
    This endpoint is used as a fallback for the frontend when the video is still processing.
    """
    from app.utils.helpers import get_video_status
    
    try:
        app.logger.info(f"Fetching direct status for video ID: {video_id}")
        status = get_video_status(video_id)
        return status
    
    except Exception as e:
        app.logger.error(f"Error checking direct video status for {video_id}: {str(e)}")
        app.logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error checking video status: {str(e)}")

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Global exception handler for the application.
    """
    app.logger.error(f"Unhandled exception: {str(exc)}")
    app.logger.error(traceback.format_exc())
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred"}
    )

# Add logger to the app for convenience
app.logger = logging.getLogger("app.main")

# Ensure required directories exist
os.makedirs("videos", exist_ok=True)
os.makedirs("audio", exist_ok=True)
os.makedirs("temp", exist_ok=True)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 