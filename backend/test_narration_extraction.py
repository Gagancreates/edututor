"""
Test script for extracting NARRATION comments from Manim code and generating a video with synchronized narration.
"""
import os
import asyncio
import logging
import json
import traceback
from pathlib import Path

from app.services.gemini import generate_manim_code
from app.services.manim import execute_manim_code_without_audio
from app.services.text_extraction import extract_narration_from_manim
from app.services.tts import generate_audio_for_script
from app.services.media_processing import merge_audio_segments_with_video

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_narration_extraction_pipeline():
    """
    Test the narration extraction pipeline using NARRATION comments from Manim code.
    """
    try:
        # Test parameters
        video_id = "test_narration_extraction"
        prompt = "Explain the quadratic formula with step-by-step visualization"
        topic = "Algebra"
        output_dir = Path(f"./temp/{video_id}")
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Step 1: Generate Manim code
        logger.info("Generating Manim code with NARRATION comments...")
        try:
            manim_code = await generate_manim_code(prompt, topic, max_retries=2, timeout=180.0)
        except Exception as e:
            logger.error(f"Failed to generate Manim code: {str(e)}")
            return False
        
        # Save the generated code
        code_path = output_dir / "code.py"
        with open(code_path, "w") as f:
            f.write(manim_code)
        logger.info(f"Saved Manim code to {code_path}")
        
        # Step 2: Extract narration from the Manim code
        logger.info("Extracting narration from Manim code...")
        script = extract_narration_from_manim(manim_code)
        
        # Save the script
        script_path = output_dir / "script.json"
        with open(script_path, "w") as f:
            json.dump(script, f, indent=2)
        logger.info(f"Saved script to {script_path}")
        
        # Print the extracted narration
        logger.info(f"Extracted {len(script)} narration segments:")
        for i, segment in enumerate(script[:3]):  # Show first 3 segments
            logger.info(f"Segment {i+1}: {segment['text'][:50]}... (duration: {segment['timing']['duration']}s)")
        
        # Step 3: Generate video from Manim code
        logger.info("Generating video from Manim code...")
        try:
            video_path = await execute_manim_code_without_audio(video_id, manim_code)
            logger.info(f"Generated video: {video_path}")
        except Exception as e:
            logger.error(f"Failed to generate video: {str(e)}")
            logger.error(traceback.format_exc())
            return False
        
        # Step 4: Generate audio for the script
        logger.info("Generating audio for the script...")
        try:
            audio_manifest = await generate_audio_for_script(script, video_id)
            
            # Save the manifest
            manifest_path = output_dir / "manifest.json"
            with open(manifest_path, "w") as f:
                json.dump(audio_manifest, f, indent=2)
            logger.info(f"Saved audio manifest to {manifest_path}")
        except Exception as e:
            logger.error(f"Error generating audio: {str(e)}")
            logger.error(traceback.format_exc())
            return False
        
        # Step 5: Merge audio and video
        logger.info("Merging audio and video...")
        try:
            output_path = await merge_audio_segments_with_video(
                video_path=video_path,
                audio_manifest=audio_manifest,
                output_path=output_dir / "final_video.mp4"
            )
            
            if output_path and os.path.exists(output_path):
                logger.info(f"Successfully created final video: {output_path}")
                return True
            else:
                logger.error("Failed to create final video")
                return False
        except Exception as e:
            logger.error(f"Error merging audio and video: {str(e)}")
            logger.error(traceback.format_exc())
            return False
            
    except Exception as e:
        logger.error(f"Test failed with error: {str(e)}")
        logger.error(traceback.format_exc())
        return False

# Example Manim code with NARRATION comments for testing
EXAMPLE_MANIM_CODE = """
from manim import *

class CreateScene(Scene):
    def construct(self):
        # NARRATION: Welcome to this lesson on the quadratic formula. 
        # We'll explore how to solve quadratic equations step by step.
        title = Text("The Quadratic Formula", color=BLUE).scale(1.2)
        self.play(Write(title))
        self.wait(2)
        
        # NARRATION: A quadratic equation has the standard form ax² + bx + c = 0,
        # where a, b, and c are constants and a is not equal to zero.
        equation = MathTex(r"ax^2 + bx + c = 0").scale(1.2)
        self.play(FadeOut(title))
        self.play(Write(equation))
        self.wait(2)
        
        # NARRATION: The quadratic formula gives us the solutions to this equation.
        # The formula is x equals negative b plus or minus the square root of b squared minus 4ac,
        # all divided by 2a.
        formula = MathTex(r"x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}").scale(1.2)
        self.play(Transform(equation, formula))
        self.wait(3)
        
        # NARRATION: Let's break down each part of this formula to understand it better.
        self.play(FadeOut(equation))
        self.wait(1)
        
        # NARRATION: First, we start with our quadratic equation in standard form.
        # Let's use a specific example: x² + 5x + 6 = 0
        example = MathTex(r"x^2 + 5x + 6 = 0").scale(1.2)
        self.play(Write(example))
        self.wait(2)
        
        # NARRATION: In this example, a equals 1, b equals 5, and c equals 6.
        values = MathTex(r"a = 1, b = 5, c = 6").scale(1.2).next_to(example, DOWN)
        self.play(Write(values))
        self.wait(2)
        
        # NARRATION: Now we substitute these values into the quadratic formula.
        # x equals negative 5 plus or minus the square root of 5 squared minus 4 times 1 times 6,
        # all divided by 2 times 1.
        substitution = MathTex(r"x = \\frac{-5 \\pm \\sqrt{5^2 - 4 \\cdot 1 \\cdot 6}}{2 \\cdot 1}").scale(1.2)
        self.play(FadeOut(example, values))
        self.play(Write(substitution))
        self.wait(3)
        
        # NARRATION: Let's simplify. 5 squared is 25, and 4 times 1 times 6 is 24.
        # So we have x equals negative 5 plus or minus the square root of 25 minus 24,
        # all divided by 2.
        simplification1 = MathTex(r"x = \\frac{-5 \\pm \\sqrt{25 - 24}}{2}").scale(1.2)
        self.play(Transform(substitution, simplification1))
        self.wait(2)
        
        # NARRATION: Further simplifying, 25 minus 24 equals 1.
        # So we have x equals negative 5 plus or minus the square root of 1,
        # all divided by 2.
        simplification2 = MathTex(r"x = \\frac{-5 \\pm \\sqrt{1}}{2}").scale(1.2)
        self.play(Transform(substitution, simplification2))
        self.wait(2)
        
        # NARRATION: The square root of 1 is 1, so our formula simplifies to
        # x equals negative 5 plus or minus 1, all divided by 2.
        simplification3 = MathTex(r"x = \\frac{-5 \\pm 1}{2}").scale(1.2)
        self.play(Transform(substitution, simplification3))
        self.wait(2)
        
        # NARRATION: This gives us two solutions:
        # x equals negative 5 plus 1 divided by 2, which is negative 2,
        # or x equals negative 5 minus 1 divided by 2, which is negative 3.
        solutions = MathTex(r"x = -2 \\text{ or } x = -3").scale(1.2)
        self.play(Transform(substitution, solutions))
        self.wait(2)
        
        # NARRATION: Let's verify these solutions by substituting them back into the original equation.
        self.play(FadeOut(substitution))
        self.wait(1)
        
        # NARRATION: Thank you for watching this explanation of the quadratic formula.
        # Now you can solve any quadratic equation using this powerful tool.
        conclusion = Text("Quadratic Formula: A Powerful Tool", color=GREEN).scale(1.2)
        self.play(Write(conclusion))
        self.wait(2)
        
        # Clean up
        self.play(FadeOut(*self.mobjects))
"""

async def test_with_example_code():
    """
    Test the narration extraction pipeline using the example Manim code.
    """
    try:
        # Test parameters
        video_id = "test_narration_example"
        output_dir = Path(f"./temp/{video_id}")
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Save the example code
        code_path = output_dir / "code.py"
        with open(code_path, "w") as f:
            f.write(EXAMPLE_MANIM_CODE)
        logger.info(f"Saved example Manim code to {code_path}")
        
        # Extract narration from the example code
        logger.info("Extracting narration from example Manim code...")
        script = extract_narration_from_manim(EXAMPLE_MANIM_CODE)
        
        # Save the script
        script_path = output_dir / "script.json"
        with open(script_path, "w") as f:
            json.dump(script, f, indent=2)
        logger.info(f"Saved script to {script_path}")
        
        # Print the extracted narration
        logger.info(f"Extracted {len(script)} narration segments:")
        for i, segment in enumerate(script):
            logger.info(f"Segment {i+1}: {segment['text'][:50]}... (duration: {segment['timing']['duration']}s)")
        
        # Generate video from the example code
        logger.info("Generating video from example Manim code...")
        try:
            video_path = await execute_manim_code_without_audio(video_id, EXAMPLE_MANIM_CODE)
            logger.info(f"Generated video: {video_path}")
        except Exception as e:
            logger.error(f"Failed to generate video: {str(e)}")
            logger.error(traceback.format_exc())
            return False
        
        # Generate audio for the script
        logger.info("Generating audio for the script...")
        try:
            audio_manifest = await generate_audio_for_script(script, video_id)
            
            # Save the manifest
            manifest_path = output_dir / "manifest.json"
            with open(manifest_path, "w") as f:
                json.dump(audio_manifest, f, indent=2)
            logger.info(f"Saved audio manifest to {manifest_path}")
        except Exception as e:
            logger.error(f"Error generating audio: {str(e)}")
            logger.error(traceback.format_exc())
            return False
        
        # Merge audio and video
        logger.info("Merging audio and video...")
        try:
            output_path = await merge_audio_segments_with_video(
                video_path=video_path,
                audio_manifest=audio_manifest,
                output_path=output_dir / "final_video.mp4"
            )
            
            if output_path and os.path.exists(output_path):
                logger.info(f"Successfully created final video: {output_path}")
                return True
            else:
                logger.error("Failed to create final video")
                return False
        except Exception as e:
            logger.error(f"Error merging audio and video: {str(e)}")
            logger.error(traceback.format_exc())
            return False
            
    except Exception as e:
        logger.error(f"Test failed with error: {str(e)}")
        logger.error(traceback.format_exc())
        return False

if __name__ == "__main__":
    print("=== Testing NARRATION extraction with Gemini-generated code ===")
    result1 = asyncio.run(test_narration_extraction_pipeline())
    
    print("\n=== Testing NARRATION extraction with example code ===")
    result2 = asyncio.run(test_with_example_code())
    
    if result1 and result2:
        print("✅ All tests completed successfully!")
    else:
        print("❌ Some tests failed!") 