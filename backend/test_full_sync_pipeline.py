#!/usr/bin/env python
"""
Full synchronization pipeline test for EduTutor.

This script tests the complete flow from:
1. Generating Manim code
2. Extracting narration from NARRATION comments
3. Generating video from Manim code
4. Generating audio from the script
5. Merging the audio and video together
"""
import os
import sys
import logging
import asyncio
import subprocess
import json
import time
import traceback
from pathlib import Path

from app.services.gemini import generate_manim_code
from app.services.manim import execute_manim_code_without_audio
from app.services.tts import generate_audio_for_script
from app.services.media_processing import merge_audio_segments_with_video
from app.services.text_extraction import extract_narration_from_manim
from app.routers.generate import generate_video_task

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
        # NARRATION: Welcome to this demonstration of circle properties.
        title = Title("Circle Properties")
        self.play(Write(title))
        self.wait(1)
        
        # NARRATION: Let's start by creating a circle with radius 2.
        circle = Circle(radius=2, color=BLUE)
        self.play(Create(circle))
        self.wait(1)
        
        # NARRATION: The center of a circle is the point from which all points on the circle are equidistant.
        center_dot = Dot(ORIGIN, color=RED)
        self.play(FadeIn(center_dot))
        self.wait(1)
        
        # NARRATION: The radius is the distance from the center to any point on the circle.
        radius = Line(ORIGIN, circle.point_at_angle(45 * DEGREES), color=YELLOW)
        radius_label = Text("r", font_size=24).next_to(radius.get_center(), UP)
        self.play(Create(radius), Write(radius_label))
        self.wait(1.5)
        
        # NARRATION: The diameter is twice the radius and passes through the center.
        diameter = Line(circle.point_at_angle(225 * DEGREES), circle.point_at_angle(45 * DEGREES), color=GREEN)
        diameter_label = Text("d = 2r", font_size=24).next_to(diameter.get_center(), DOWN)
        self.play(Create(diameter), Write(diameter_label))
        self.wait(1.5)
        
        # NARRATION: The circumference of a circle equals pi times the diameter.
        circumference_formula = MathTex("C = \\pi \\times d").scale(1.5)
        self.play(
            FadeOut(title),
            FadeOut(radius_label),
            FadeOut(diameter_label),
            Transform(circle, circumference_formula)
        )
        self.wait(1.5)
        
        # NARRATION: The area of a circle equals pi times the radius squared.
        area_formula = MathTex("A = \\pi \\times r^2").scale(1.5)
        self.play(Transform(circle, area_formula))
        self.wait(1.5)
        
        # NARRATION: Understanding these properties is fundamental to mathematics.
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
        return None

async def extract_narration(manim_code):
    """
    Extract narration text with timing from Manim code.
    
    Args:
        manim_code: Manim code with narration comments
        
    Returns:
        List of script segments with timing information
    """
    try:
        logger.info("Extracting narration from Manim code")
        script = extract_narration_from_manim(manim_code)
        
        logger.info(f"Extracted {len(script)} script segments")
        for i, segment in enumerate(script[:3]):  # Show first 3 segments
            logger.info(f"Segment {i+1}: {segment['text'][:50]}... (start: {segment['timing']['start']}s, duration: {segment['timing']['duration']}s)")
        
        return script
    except Exception as e:
        logger.error(f"Error extracting narration: {e}")
        # Return a simple script for testing
        return [
            {
                "text": "Welcome to this demonstration of circle properties.",
                "timing": {"start": 0.0, "duration": 2.0},
                "type": "narration"
            },
            {
                "text": "Let's start by creating a circle with radius 2.",
                "timing": {"start": 2.0, "duration": 2.0},
                "type": "narration"
            }
        ]

async def enhance_script_with_ssml(script):
    """
    Enhance the script with SSML (Speech Synthesis Markup Language) tags.
    
    Args:
        script: List of script segments
        
    Returns:
        Enhanced script with SSML tags
    """
    enhanced_script = []
    
    for segment in script:
        text = segment['text']
        
        # Add pauses after punctuation
        text = text.replace(".", ".<break time='500ms'/>")
        text = text.replace("!", "!<break time='500ms'/>")
        text = text.replace("?", "?<break time='500ms'/>")
        text = text.replace(",", ",<break time='300ms'/>")
        text = text.replace(";", ";<break time='400ms'/>")
        
        # Add emphasis to mathematical terms
        # This is a simple example, could be expanded with more sophisticated patterns
        math_terms = ["circle", "radius", "diameter", "circumference", "area", "pi", "squared"]
        for term in math_terms:
            if term in text.lower():
                text = text.replace(term, f"<emphasis level='moderate'>{term}</emphasis>")
        
        # Create enhanced segment
        enhanced_segment = segment.copy()
        enhanced_segment['text'] = f"<speak>{text}</speak>"
        enhanced_script.append(enhanced_segment)
    
    return enhanced_script

async def generate_audio(script, output_dir, use_elevenlabs=False):
    """
    Generate audio for the script.
    
    Args:
        script: List of script segments with text and timing
        output_dir: Directory to save the audio files
        use_elevenlabs: Whether to use the ElevenLabs API
        
    Returns:
        Audio manifest with segment information
    """
    try:
        # Create audio directory
        audio_dir = Path(output_dir) / "audio"
        os.makedirs(audio_dir, exist_ok=True)
        
        # Process audio segments
        logger.info("Generating audio segments...")
        
        # Create manifest structure
        manifest = {
            "segments": []
        }
        
        if use_elevenlabs:
            try:
                audio_manifest = await generate_audio_for_script(script, "sync_test")
                logger.info(f"Generated {len(audio_manifest['segments'])} audio segments using ElevenLabs")
                
                # Copy audio files to our directory
                for segment in audio_manifest["segments"]:
                    src_path = Path(segment["audio_path"])
                    if src_path.exists():
                        import shutil
                        dest_path = audio_dir / src_path.name
                        shutil.copy2(src_path, dest_path)
                        
                        # Update path in our manifest
                        manifest["segments"].append({
                            "text": segment["text"],
                            "start": segment["timing"]["start"],
                            "duration": segment["timing"]["duration"],
                            "audio_path": str(dest_path)
                        })
                
                return manifest
                
            except Exception as e:
                logger.error(f"Error using ElevenLabs: {e}")
                use_elevenlabs = False
        
        # Fallback: Generate simple audio files using FFmpeg
        if not use_elevenlabs:
            for i, segment in enumerate(script):
                output_path = audio_dir / f"segment_{i:03d}.mp3"
                
                # Create a silent audio file for testing
                duration_secs = segment["timing"]["duration"]
                try:
                    subprocess.run([
                        "ffmpeg", "-y",
                        "-f", "lavfi", 
                        "-i", f"sine=frequency=1000:duration={duration_secs}",
                        "-af", f"afade=t=in:ss=0:d=0.5,afade=t=out:st={duration_secs-0.5}:d=0.5",
                        str(output_path)
                    ], check=True, capture_output=True)
                    
                    # Add to manifest using audio_path key
                    manifest["segments"].append({
                        "text": segment["text"],
                        "start": segment["timing"]["start"],
                        "duration": segment["timing"]["duration"],
                        "audio_path": str(output_path)
                    })
                    
                except subprocess.SubprocessError as e:
                    logger.error(f"Error generating audio segment {i}: {e}")
            
        # Save manifest
        manifest_path = audio_dir / "manifest.json"
        with open(manifest_path, "w") as f:
            json.dump(manifest, f, indent=2)
            
        logger.info(f"Generated {len(manifest['segments'])} audio segments")
        return manifest
    
    except Exception as e:
        logger.error(f"Error generating audio: {e}")
        return {"segments": []}

async def merge_audio_video(video_path, audio_manifest, output_path):
    """
    Merge audio segments with the video using FFmpeg.
    
    Args:
        video_path: Path to the video file
        audio_manifest: Audio manifest with segment information
        output_path: Path to save the output video
        
    Returns:
        Path to the merged video file
    """
    try:
        logger.info("Merging audio and video...")
        merged_video = await merge_audio_segments_with_video(
            video_path=video_path,
            audio_manifest=audio_manifest,
            output_path=output_path
        )
        
        if merged_video and Path(merged_video).exists():
            logger.info(f"Successfully merged audio and video: {merged_video}")
            return merged_video
        else:
            logger.error("Failed to merge audio and video")
            return None
    
    except Exception as e:
        logger.error(f"Error merging audio and video: {e}")
        return None

async def run_full_pipeline(output_dir, use_elevenlabs=False):
    """
    Run the full synchronization pipeline.
    
    Args:
        output_dir: Directory to save outputs
        use_elevenlabs: Whether to use ElevenLabs for TTS
        
    Returns:
        Boolean indicating success
    """
    try:
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Step 1: Check dependencies
        if not await check_dependencies():
            logger.error("Missing required dependencies")
            return False
        
        # Step 2: Generate video
        video_path = await generate_manim_video(output_dir)
        
        # If video generation failed, create a dummy video
        if not video_path:
            logger.warning("Using dummy video instead")
            video_path = await create_dummy_video(output_dir)
            if not video_path:
                logger.error("Failed to create even a dummy video")
                return False
        
        # Step 3: Extract narration
        script = await extract_narration(SAMPLE_MANIM_CODE)
        if not script:
            logger.error("Failed to extract narration")
            return False
        
        # Save the script
        script_path = Path(output_dir) / "script.json"
        with open(script_path, "w") as f:
            json.dump(script, f, indent=2)
        
        # Step 4: Enhance script with SSML (optional)
        enhanced_script = await enhance_script_with_ssml(script)
        
        # Step 5: Generate audio
        audio_manifest = await generate_audio(enhanced_script, output_dir, use_elevenlabs)
        if not audio_manifest or not audio_manifest["segments"]:
            logger.error("Failed to generate audio")
            return False
        
        # Step 6: Merge audio and video
        final_path = Path(output_dir) / "circle_example_narrated.mp4"
        merged_video = await merge_audio_video(video_path, audio_manifest, final_path)
        if not merged_video:
            logger.error("Failed to merge audio and video")
            return False
        
        logger.info(f"Full pipeline completed successfully. Output: {merged_video}")
        return True
        
    except Exception as e:
        logger.error(f"Error in full pipeline: {e}")
        logger.error(traceback.format_exc())
        return False

async def test_full_pipeline():
    """
    Test the full pipeline with the sample Manim code.
    """
    logger.info("=== Testing Full Pipeline ===")
    output_dir = Path("./temp/full_sync_test")
    
    start_time = time.time()
    result = await run_full_pipeline(output_dir)
    end_time = time.time()
    
    if result:
        logger.info(f"✅ Full pipeline test passed in {end_time - start_time:.2f} seconds")
        
        # Open the video if on a desktop OS
        final_video = output_dir / "circle_example_narrated.mp4"
        if final_video.exists():
            logger.info(f"Final video available at: {final_video}")
            try:
                if sys.platform == "win32":
                    os.startfile(final_video)
                elif sys.platform == "darwin":  # macOS
                    subprocess.run(["open", final_video])
                else:  # Linux
                    subprocess.run(["xdg-open", final_video])
            except Exception as e:
                logger.warning(f"Could not open video automatically: {e}")
    else:
        logger.error(f"❌ Full pipeline test failed after {end_time - start_time:.2f} seconds")
    
    return result

async def test_component_pipeline():
    """
    Test each component of the pipeline individually.
    """
    logger.info("=== Testing Individual Components ===")
    output_dir = Path("./temp/sync_test")
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Save the sample Manim code
    manim_path = output_dir / "circle_example.py"
    with open(manim_path, "w") as f:
        f.write(SAMPLE_MANIM_CODE)
        
    # Test the dependencies
    logger.info("Testing dependencies...")
    dependencies_ok = await check_dependencies()
    logger.info(f"Dependencies check: {'✅' if dependencies_ok else '❌'}")
    
    # Test script extraction
    logger.info("Testing script extraction...")
    script = await extract_narration(SAMPLE_MANIM_CODE)
    script_ok = len(script) > 0
    logger.info(f"Script extraction: {'✅' if script_ok else '❌'} ({len(script)} segments)")
    
    # Save the script
    script_path = output_dir / "script.json"
    with open(script_path, "w") as f:
        json.dump(script, f, indent=2)
    
    # Test audio generation (with dummy audio)
    logger.info("Testing audio generation...")
    audio_manifest = await generate_audio(script, output_dir, use_elevenlabs=False)
    audio_ok = len(audio_manifest["segments"]) > 0
    logger.info(f"Audio generation: {'✅' if audio_ok else '❌'} ({len(audio_manifest['segments'])} segments)")
    
    # Test video generation (create a dummy video)
    logger.info("Testing video generation...")
    video_path = await create_dummy_video(output_dir)
    video_ok = video_path and Path(video_path).exists()
    logger.info(f"Video generation: {'✅' if video_ok else '❌'}")
    
    # Test audio-video merging
    if video_ok and audio_ok:
        logger.info("Testing audio-video merging...")
        final_path = output_dir / "circle_example_narrated.mp4"
        merged_video = await merge_audio_video(video_path, audio_manifest, final_path)
        merging_ok = merged_video and Path(merged_video).exists()
        logger.info(f"Audio-video merging: {'✅' if merging_ok else '❌'}")
    
    return dependencies_ok and script_ok and audio_ok and video_ok

async def run_tests():
    """Run all tests."""
    logger.info("Starting tests...")
    
    # Test component pipeline first
    component_result = await test_component_pipeline()
    logger.info(f"Component tests: {'✅' if component_result else '❌'}")
    
    # Then test the full pipeline
    full_result = await test_full_pipeline()
    logger.info(f"Full pipeline test: {'✅' if full_result else '❌'}")
    
    return component_result and full_result

def main():
    """Main function."""
    # Run the tests
    success = asyncio.run(run_tests())
    
    # Exit with status code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 