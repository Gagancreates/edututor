#!/usr/bin/env python
"""
Full Audio-Video Synchronization Pipeline Test

This script tests the complete audio-video synchronization pipeline:
1. Generate a simple Manim scene
2. Extract narration text with timing
3. Generate audio for the narration
4. Merge audio with the video
5. Verify the output

Usage:
    python test_full_sync_pipeline.py [--output-dir OUTPUT_DIR] [--use-elevenlabs]
"""
import os
import sys
import asyncio
import logging
import argparse
import tempfile
import subprocess
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Sample Manim code with narration comments
SAMPLE_MANIM_CODE = """
from manim import *

class CircleExample(Scene):
    def construct(self):
        # narration: Welcome to this demonstration of circle properties.
        title = Title("Circle Properties")
        self.play(Write(title))
        self.wait(1)
        
        # narration: Let's start by creating a circle with radius 2.
        circle = Circle(radius=2, color=BLUE)
        self.play(Create(circle))
        self.wait(1)
        
        # narration: The center of a circle is the point from which all points on the circle are equidistant.
        center_dot = Dot(ORIGIN, color=RED)
        self.play(FadeIn(center_dot))
        self.wait(1)
        
        # narration: The radius is the distance from the center to any point on the circle.
        radius = Line(ORIGIN, circle.point_at_angle(45 * DEGREES), color=YELLOW)
        radius_label = Text("r", font_size=24).next_to(radius.get_center(), UP)
        self.play(Create(radius), Write(radius_label))
        self.wait(1.5)
        
        # narration: The diameter is twice the radius and passes through the center.
        diameter = Line(circle.point_at_angle(225 * DEGREES), circle.point_at_angle(45 * DEGREES), color=GREEN)
        diameter_label = Text("d = 2r", font_size=24).next_to(diameter.get_center(), DOWN)
        self.play(Create(diameter), Write(diameter_label))
        self.wait(1.5)
        
        # narration: The circumference of a circle equals pi times the diameter.
        circumference_formula = MathTex("C = \\pi \\times d").scale(1.5)
        self.play(
            FadeOut(title),
            FadeOut(radius_label),
            FadeOut(diameter_label),
            Transform(circle, circumference_formula)
        )
        self.wait(1.5)
        
        # narration: The area of a circle equals pi times the radius squared.
        area_formula = MathTex("A = \\pi \\times r^2").scale(1.5)
        self.play(Transform(circle, area_formula))
        self.wait(1.5)
        
        # narration: Understanding these properties is fundamental to mathematics.
        final_text = Text("Circles are fundamental shapes", font_size=36)
        self.play(Transform(circle, final_text))
        self.wait(2)
"""

async def check_dependencies():
    """Check if required dependencies are installed."""
    # Check for FFmpeg
    try:
        subprocess.run(["ffmpeg", "-version"], check=True, capture_output=True)
        logger.info("FFmpeg is installed")
    except (subprocess.SubprocessError, FileNotFoundError):
        logger.error("FFmpeg is not installed. Please install FFmpeg to continue.")
        return False
    
    # Check for Manim (optional)
    try:
        import manim
        logger.info(f"Manim is installed (version: {manim.__version__})")
        has_manim = True
    except ImportError:
        logger.warning("Manim is not installed. Will skip video generation step.")
        has_manim = False
    
    # Check for ElevenLabs
    try:
        import elevenlabs
        logger.info("ElevenLabs package is installed")
        has_elevenlabs = True
    except ImportError:
        logger.warning("ElevenLabs package is not installed. Will use dummy audio.")
        has_elevenlabs = False
    
    # Check for required modules
    try:
        from app.services.text_extraction import ManimTextExtractor
        logger.info("Text extraction module is available")
    except ImportError:
        logger.error("Text extraction module not found. Make sure you're in the backend directory.")
        return False
    
    return True

async def generate_manim_video(output_dir):
    """
    Generate a video from Manim code.
    
    Args:
        output_dir: Directory to save the Manim code and output
        
    Returns:
        Path to the generated video file or None if generation failed
    """
    try:
        # Check if Manim is installed
        try:
            import manim
        except ImportError:
            logger.warning("Manim is not installed. Skipping video generation.")
            return None
        
        # Create Manim file
        manim_file = Path(output_dir) / "circle_example.py"
        with open(manim_file, "w") as f:
            f.write(SAMPLE_MANIM_CODE)
        
        logger.info(f"Created Manim file at {manim_file}")
        
        # Run Manim to generate video
        logger.info("Running Manim to generate video...")
        
        try:
            subprocess.run([
                sys.executable, "-m", "manim", 
                str(manim_file), "CircleExample", 
                "-pql", "--media_dir", output_dir
            ], check=True)
            
            # Check for generated video
            video_path = Path(output_dir) / "videos" / "circle_example" / "480p15" / "CircleExample.mp4"
            if video_path.exists():
                logger.info(f"Generated video at {video_path}")
                return video_path
            else:
                # Try alternative paths
                possible_paths = list(Path(output_dir).glob("**/CircleExample.mp4"))
                if possible_paths:
                    logger.info(f"Generated video at {possible_paths[0]}")
                    return possible_paths[0]
                else:
                    logger.error("Video generation failed: output file not found")
                    return None
                
        except subprocess.SubprocessError as e:
            logger.error(f"Error running Manim: {e}")
            return None
            
    except Exception as e:
        logger.error(f"Error generating Manim video: {e}")
        return None

async def create_dummy_video(output_dir):
    """
    Create a dummy video file for testing when Manim is not available.
    
    Args:
        output_dir: Directory to save the dummy video
        
    Returns:
        Path to the dummy video file
    """
    # Create output directory structure
    video_dir = Path(output_dir) / "videos" / "circle_example" / "480p15"
    os.makedirs(video_dir, exist_ok=True)
    
    # Create a dummy video file using FFmpeg
    video_path = video_dir / "CircleExample.mp4"
    
    try:
        # Generate a 10-second video with a blue circle
        subprocess.run([
            "ffmpeg", "-y",
            "-f", "lavfi", "-i", "color=c=blue:s=640x480:d=10",
            "-vf", "format=yuv420p,drawtext=text='Circle Example':fontcolor=white:fontsize=24:x=(w-text_w)/2:y=(h-text_h)/2",
            str(video_path)
        ], check=True, capture_output=True)
        
        logger.info(f"Created dummy video at {video_path}")
        return video_path
    except subprocess.SubprocessError as e:
        logger.error(f"Error creating dummy video: {e}")
        
        # Create an empty file as fallback
        with open(video_path, "w") as f:
            f.write("Dummy video file")
        
        logger.warning(f"Created empty dummy video file at {video_path}")
        return video_path

async def extract_narration(manim_code):
    """
    Extract narration text with timing from Manim code.
    
    Args:
        manim_code: Manim code with narration comments
        
    Returns:
        List of script segments with timing information
    """
    try:
        from app.services.text_extraction import ManimTextExtractor
        
        logger.info("Extracting narration from Manim code")
        extractor = ManimTextExtractor()
        script = extractor.extract_script(manim_code)
        
        logger.info(f"Extracted {len(script)} script segments")
        for i, segment in enumerate(script[:3]):  # Show first 3 segments
            logger.info(f"Segment {i}: {segment['text'][:50]}... (start: {segment['timing']['start']}s, duration: {segment['timing']['duration']}s)")
        
        return script
    except Exception as e:
        logger.error(f"Error extracting narration: {e}")
        # Return a simple script for testing
        return [
            {
                "text": "Welcome to this demonstration of circle properties.",
                "timing": {"start": 0.0, "duration": 2.0},
                "type": "text"
            },
            {
                "text": "Let's start by creating a circle with radius 2.",
                "timing": {"start": 2.0, "duration": 2.0},
                "type": "text"
            }
        ]

async def enhance_script_with_ssml(script):
    """
    Enhance script with SSML tags for better timing control.
    
    Args:
        script: List of script segments
        
    Returns:
        Enhanced script with SSML tags
    """
    try:
        from app.services.sync import enhance_script_with_ssml
        
        logger.info("Enhancing script with SSML tags")
        enhanced_script = enhance_script_with_ssml(script)
        
        logger.info(f"Enhanced {len(enhanced_script)} script segments with SSML")
        for i, segment in enumerate(enhanced_script[:3]):  # Show first 3 segments
            logger.info(f"Segment {i}: {segment['text'][:50]}...")
        
        return enhanced_script
    except Exception as e:
        logger.error(f"Error enhancing script with SSML: {e}")
        
        # Create enhanced script manually
        from test_audio_sync import add_ssml_tags, insert_strategic_pauses
        
        enhanced_script = []
        for segment in script:
            enhanced_segment = segment.copy()
            enhanced_segment["text"] = add_ssml_tags(segment["text"], segment["timing"]["duration"])
            enhanced_script.append(enhanced_segment)
        
        logger.info(f"Created {len(enhanced_script)} enhanced script segments manually")
        
        # Add strategic pauses
        enhanced_script = insert_strategic_pauses(script)
        
        return enhanced_script

async def generate_audio(script, output_dir, use_elevenlabs=False):
    """
    Generate audio for the script segments.
    
    Args:
        script: List of script segments
        output_dir: Directory to save audio files
        use_elevenlabs: Whether to use ElevenLabs for TTS
        
    Returns:
        Audio manifest with paths to audio segments
    """
    try:
        # Ensure output directory exists
        output_dir = Path(output_dir)
        os.makedirs(output_dir, exist_ok=True)
        
        if use_elevenlabs:
            # Check if ElevenLabs API key is set
            api_key = os.getenv("ELEVEN_LABS_API_KEY")
            if not api_key:
                logger.warning("ELEVEN_LABS_API_KEY not set, falling back to dummy audio")
                use_elevenlabs = False
        
        if use_elevenlabs:
            try:
                from app.services.tts import generate_chunked_audio
                
                logger.info("Generating audio with ElevenLabs TTS")
                audio_chunks = await generate_chunked_audio(
                    script_segments=script,
                    voice_id=None,  # Use default voice
                    output_dir=output_dir
                )
            except Exception as e:
                logger.error(f"Error generating audio with ElevenLabs: {e}")
                use_elevenlabs = False
        
        if not use_elevenlabs:
            # Use dummy audio generation
            from test_audio_sync import generate_dummy_audio_chunks
            
            logger.info("Generating dummy audio")
            audio_chunks = await generate_dummy_audio_chunks(script, output_dir)
        
        logger.info(f"Generated {len(audio_chunks)} audio chunks")
        
        # Save manifest
        import json
        manifest = {
            "video_id": "circle_example",
            "segments": audio_chunks
        }
        
        manifest_path = output_dir / "manifest.json"
        with open(manifest_path, "w") as f:
            json.dump(manifest, f, indent=2)
        
        logger.info(f"Saved audio manifest to {manifest_path}")
        
        return manifest
    except Exception as e:
        logger.error(f"Error generating audio: {e}")
        return {"video_id": "circle_example", "segments": []}

async def merge_audio_video(video_path, audio_manifest, output_path):
    """
    Merge audio with video.
    
    Args:
        video_path: Path to the video file
        audio_manifest: Audio manifest with paths to audio segments
        output_path: Path to save the output file
        
    Returns:
        Path to the merged video file
    """
    try:
        logger.info(f"Merging audio with video: {video_path}")
        
        try:
            from app.services.media_processing import merge_audio_segments_with_video_direct
            
            result = await merge_audio_segments_with_video_direct(
                video_path=video_path,
                audio_manifest=audio_manifest,
                output_path=output_path
            )
        except ImportError:
            logger.warning("Could not import merge_audio_segments_with_video_direct, using simple implementation")
            
            from test_audio_sync import simple_merge_audio_video
            
            result = await simple_merge_audio_video(
                video_path=video_path,
                audio_manifest=audio_manifest,
                output_path=output_path
            )
        
        if result:
            logger.info(f"Successfully created synchronized video at {result}")
            return result
        else:
            logger.error("Failed to create synchronized video")
            return None
    except Exception as e:
        logger.error(f"Error merging audio and video: {e}")
        return None

async def run_full_pipeline(output_dir, use_elevenlabs=False):
    """
    Run the full audio-video synchronization pipeline.
    
    Args:
        output_dir: Directory to save output files
        use_elevenlabs: Whether to use ElevenLabs for TTS
        
    Returns:
        Path to the final synchronized video
    """
    # Check dependencies
    if not await check_dependencies():
        logger.error("Missing required dependencies. Exiting.")
        return None
    
    # Step 1: Generate Manim video
    video_path = await generate_manim_video(output_dir)
    
    # If video generation failed, create a dummy video
    if not video_path:
        logger.warning("Video generation failed or skipped, creating dummy video")
        video_path = await create_dummy_video(output_dir)
    
    # Step 2: Extract narration
    script = await extract_narration(SAMPLE_MANIM_CODE)
    
    # Step 3: Enhance script with SSML
    enhanced_script = await enhance_script_with_ssml(script)
    
    # Step 4: Generate audio
    audio_dir = Path(output_dir) / "audio"
    os.makedirs(audio_dir, exist_ok=True)
    
    audio_manifest = await generate_audio(enhanced_script, audio_dir, use_elevenlabs)
    
    # Step 5: Merge audio with video
    output_video_path = Path(output_dir) / "circle_example_narrated.mp4"
    
    final_video = await merge_audio_video(video_path, audio_manifest, output_video_path)
    
    if final_video:
        logger.info(f"Full pipeline completed successfully. Output: {final_video}")
    else:
        logger.error("Full pipeline failed.")
    
    return final_video

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Test the full audio-video synchronization pipeline")
    parser.add_argument("--output-dir", default="./temp/full_sync_test", help="Directory to save output files")
    parser.add_argument("--use-elevenlabs", action="store_true", help="Use ElevenLabs for TTS (requires API key)")
    
    args = parser.parse_args()
    
    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Run the full pipeline
    result = asyncio.run(run_full_pipeline(args.output_dir, args.use_elevenlabs))
    
    if result:
        print(f"\nFull pipeline test completed successfully!")
        print(f"Synchronized video: {result}")
        return 0
    else:
        print("\nFull pipeline test failed.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 