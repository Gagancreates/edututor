"""
Gemini API integration for generating Manim code.
"""
import os
import logging
import traceback
import google.generativeai as genai
from typing import Optional
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Configure the Gemini API
try:
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
    if not GEMINI_API_KEY:
        logger.warning("GEMINI_API_KEY not found in environment variables")
        logger.warning("Please run 'python setup_env.py' to set up your API key")
    else:
        genai.configure(api_key=GEMINI_API_KEY)
        logger.info("Gemini API configured successfully")
except Exception as e:
    logger.error(f"Error configuring Gemini API: {str(e)}")

async def generate_manim_code(prompt: str, topic: Optional[str] = None, grade_level: Optional[str] = None, duration_minutes: float = 3.0) -> str:
    """
    Generate Manim code using the Gemini API.
    
    Args:
        prompt: The prompt for generating the video
        topic: The educational topic (optional)
        grade_level: The target grade level (optional)
        duration_minutes: The desired duration in minutes (default: 3.0)
        
    Returns:
        Generated Manim Python code
    """
    try:
        logger.info(f"Generating Manim code for prompt: {prompt}")
        
        # Check if API key is configured
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not set. Please run 'python setup_env.py' to configure.")
        
        # Construct a more detailed prompt with specific instructions
        detailed_prompt = f"""
Generate Python code using the Manim library to create an educational animation about {topic if topic else 'the following topic'}: {prompt}.
{f'The target audience is {grade_level} students.' if grade_level else ''}
The animation should be approximately {duration_minutes} minutes long.

IMPORTANT INSTRUCTIONS:
1. DO NOT include any Markdown formatting (no ```python or ``` tags).
2. Return ONLY the pure Python code, no explanations or comments outside the code.
3. The main scene class MUST be named 'CreateScene' and MUST inherit ONLY from Scene class, not any other class like ZoomedScene.
4. Include proper imports at the top (from manim import *).
5. Use only standard Manim features (no custom libraries).
6. Include educational text, formulas, and visual elements.
7. Make smooth transitions between concepts.
8. Add appropriate colors, animations, and visual appeal.
9. Ensure the code is complete, error-free, and ready to execute.
10. Include helpful comments within the code to explain key parts.

CRITICAL RESTRICTIONS TO AVOID ERRORS:
0.Do not use any external assets like images, videos, or audio files.
1. DO NOT use 'display_frame' parameter in any Scene initialization.
2. DO NOT use ZoomedScene, ThreeDScene, or other specialized scene types - ONLY use the basic Scene class.
3. DO NOT use TransformMatchingTex on objects that are not Tex or MathTex objects.
4. DO NOT attempt to access 'tex_string' attribute on objects that aren't Tex-based.
5. DO NOT use any deprecated Manim features or syntax.
6. Keep animations simple and avoid complex camera movements.
7. Use ONLY these animation types: Create, Write, FadeIn, FadeOut, Transform, ReplacementTransform, and basic animations.
8. For text, use only Text() or Tex() or MathTex() classes.
9. For shapes, use only Circle, Square, Rectangle, Arrow, Line, and other basic shapes.
10. Always set appropriate run_time for animations (between 0.5 and 2 seconds).
11. Always include self.wait() between animations to give viewers time to understand.
12. End with self.play(FadeOut(*self.mobjects)) to clear the scene.

Example structure (but with YOUR content):
from manim import *

class CreateScene(Scene):
    def construct(self):
        # Introduction
        title = Text("Your Title")
        self.play(Write(title), run_time=1)
        self.wait(1)
        
        # Main content with simple animations
        # ...
        
        # Conclusion
        self.play(FadeOut(*self.mobjects), run_time=1)
"""
        
        # Generate the code using Gemini
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(detailed_prompt)
        
        # Extract the code from the response
        if not response.text:
            logger.error("Gemini API returned empty response")
            raise ValueError("Failed to generate code: Empty response from Gemini API")
        
        manim_code = response.text.strip()
        
        # Log a preview of the generated code
        logger.info(f"Generated Manim code preview: {manim_code[:500]}...")
        
        return manim_code
        
    except Exception as e:
        logger.error(f"Error generating Manim code: {str(e)}")
        logger.error(traceback.format_exc())
        raise ValueError(f"Failed to generate Manim code: {str(e)}") 