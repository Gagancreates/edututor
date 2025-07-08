"""
Router for video generation endpoints.
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
import logging
import traceback
import os
import json
import asyncio

from app.services.gemini import generate_manim_code
from app.services.manim import execute_manim_code, execute_manim_code_without_audio
from app.services.text_extraction import extract_narration_from_manim
from app.services.tts import generate_audio_for_script
from app.services.media_processing import merge_audio_segments_with_video
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

def handle_manim_generation_error(video_id: str, error: Exception, prompt: str = "", topic: str = None):
    """
    Handle errors during Manim code generation.
    
    Args:
        video_id: The ID of the video
        error: The exception that was raised
        prompt: The prompt that was used
        topic: The topic that was specified
    """
    logger.error(f"Failed to generate Manim code for video {video_id}: {str(error)}")
    logger.error(traceback.format_exc())
    
    # Create videos directory for this video_id if it doesn't exist
    video_dir = os.path.join("videos", video_id)
    os.makedirs(video_dir, exist_ok=True)
    
    # Save the error to a file
    error_file = os.path.join(video_dir, "error.txt")
    with open(error_file, "w") as f:
        error_message = f"Failed to generate Manim code: {str(error)}\n\n"
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
            "message": f"Failed to generate code: {str(error)}"
        }
        json.dump(metadata, f)
    
    logger.error(f"Generation failed for video {video_id}. Error saved to {error_file}")

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
        
        # Create videos directory for this video_id if it doesn't exist
        video_dir = os.path.join("videos", video_id)
        os.makedirs(video_dir, exist_ok=True)
        
        # STEP 1: Generate Manim code using Gemini (first LLM call)
        try:
            logger.info("Generating Manim code with NARRATION comments...")
            manim_code = await generate_manim_code(
                prompt=prompt, 
                topic=topic, 
                grade_level=grade_level, 
                duration_minutes=duration_minutes,
                max_retries=3,
                timeout=180.0  # 3 minutes timeout
            )
        except Exception as e:
            handle_manim_generation_error(video_id, e, prompt, topic)
            return
        
        # Clean the code to remove any Markdown formatting
        if "```" in manim_code:
            logger.warning("Detected Markdown code blocks in the code, cleaning...")
            manim_code = clean_code(manim_code)
        
        # Save the generated code
        code_file = os.path.join(video_dir, f"{video_id}.py")
        with open(code_file, "w") as f:
            f.write(manim_code)
        
        # STEP 2: Generate video from Manim code
        logger.info("Generating video from Manim code...")
        try:
            video_path = await execute_manim_code_without_audio(video_id, manim_code)
        except Exception as e:
            logger.error(f"Error executing Manim code: {str(e)}")
            error_file = os.path.join(video_dir, "error.txt")
            with open(error_file, "a") as f:
                f.write(f"\nError executing Manim code: {str(e)}")
            return
            
        # STEP 3: Extract narration from NARRATION comments in the Manim code
        logger.info("Extracting narration from NARRATION comments...")
        try:
            script = extract_narration_from_manim(manim_code)
            logger.info(f"Extracted {len(script)} narration segments")
            
            # Save the script
            script_path = os.path.join(video_dir, "script.json")
            with open(script_path, "w") as f:
                json.dump(script, f, indent=2)
        except Exception as e:
            logger.error(f"Error extracting narration: {str(e)}")
            logger.error(traceback.format_exc())
            
            # Create a generic script if narration extraction fails
            script = [{
                "text": "Welcome to this educational video created with Manim.",
                "timing": {
                    "start": 0.0,
                    "duration": 3.0
                },
                "type": "generic"
            }]
            logger.info("Using generic script due to extraction failure")
        
        # STEP 4: Generate audio for the script
        logger.info("Generating audio for the script...")
        try:
            audio_manifest = await generate_audio_for_script(script, video_id)
            
            # Save the manifest
            manifest_path = os.path.join(video_dir, "manifest.json")
            with open(manifest_path, "w") as f:
                json.dump(audio_manifest, f, indent=2)
        except Exception as e:
            logger.error(f"Error generating audio: {str(e)}")
            logger.error(traceback.format_exc())
            return
        
        # STEP 5: Merge audio and video
        logger.info("Merging audio and video...")
        try:
            output_path = await merge_audio_segments_with_video(
                video_path=video_path,
                audio_manifest=audio_manifest,
                output_path=os.path.join(video_dir, f"{video_id}_final.mp4")
            )
        except Exception as e:
            logger.error(f"Error merging audio and video: {str(e)}")
            logger.error(traceback.format_exc())
            return
        
        # Update metadata
        metadata_file = os.path.join(video_dir, "metadata.json")
        with open(metadata_file, "w") as f:
            metadata = {
                "status": "completed",
                "prompt": prompt,
                "topic": topic,
                "original_video": str(video_path),
                "final_video": str(output_path),
                "script_source": "narration_extraction"
            }
            json.dump(metadata, f, indent=2)
        
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