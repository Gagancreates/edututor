"""
FastAPI entry point for EduTutor backend.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pathlib import Path

from app.routers import generate
from app.utils.helpers import get_video_path

app = FastAPI(title="EduTutor API", description="API for generating educational videos using Manim")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(generate.router, prefix="/api", tags=["generate"])

@app.get("/")
async def root():
    """Root endpoint to check if API is running."""
    return {"message": "Welcome to EduTutor API", "status": "online"}

@app.get("/api/video/file/{video_id}")
async def get_video_file(video_id: str):
    """
    Serve a generated video file.
    
    Args:
        video_id: The unique ID of the video
        
    Returns:
        Video file as a streaming response
    """
    video_path = get_video_path(video_id)
    if not video_path or not video_path.exists():
        raise HTTPException(status_code=404, detail="Video not found")
    
    return FileResponse(
        path=str(video_path),
        media_type="video/mp4",
        filename=f"educational_video_{video_id}.mp4"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 