"""
Gemini API integration for generating Manim code.
"""
import os
import google.generativeai as genai

from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the Gemini API client
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set")

genai.configure(api_key=GEMINI_API_KEY)

# Select the model
model = genai.GenerativeModel('gemini-pro')

async def generate_manim_code(prompt: str) -> str:
    """
    Generate Manim code using Gemini API based on the educational prompt.
    
    Args:
        prompt: The user's educational prompt
        
    Returns:
        Generated Manim code as a string
    """
    # Default values
    complexity = "based on the prompt"
    duration = 90
    
    # Craft the prompt for Gemini
    system_prompt = f"""
    You are an expert educational content creator specializing in creating Manim animations.
    
    Your task is to create Python code using the Manim library that will generate an educational
    video explaining the concept: "{prompt}".
    
    Requirements:
    
    - Target duration: approximately {duration} seconds, can be more or less based on the prompt
    - The code should be complete, runnable, and self-contained
    - Use Manim's Scene class and appropriate animations
    - Include clear, step-by-step explanations through text and visuals
    - Focus on educational clarity and visual engagement
    - Include appropriate mathematical notation where relevant
    - The code should be optimized to run without errors
    
    IMPORTANT TECHNICAL REQUIREMENTS:
    1. Name your main scene class "CreateScene" (this is critical for execution)
    2. Use the latest Manim Community version syntax (not the deprecated ManimCE or 3b1b versions)
    3. Include ALL necessary imports at the top of the file
    4. Use proper color objects (e.g., RED, BLUE, GREEN) instead of strings
    5. Ensure all animations have appropriate run_time parameters to fit the target duration
    6. Use self.wait() with appropriate durations to give viewers time to understand concepts
    7. Add self.play(FadeOut(*self.mobjects)) at the end of the animation for clean transitions
    8. Include proper text positioning and scaling for readability
    9. For mathematical concepts, use MathTex for proper LaTeX rendering
    10. Structure the animation in logical sections with clear transitions between ideas
    
    EDUCATIONAL BEST PRACTICES:
    1. Start with a clear introduction of the concept
    2. Break down complex ideas into simpler components
    3. Use visual metaphors and analogies where appropriate
    4. Build concepts incrementally, showing the relationship between ideas
    5. Include real-world examples or applications when relevant
    6. Summarize key points at the end
    7. Use color consistently to represent specific elements or ideas
    8. Include interactive elements where appropriate (e.g., transformations, highlighting)
    
    Provide ONLY the Python code without any additional explanations or markdown.
    The code should start with imports and end with the scene class.
    """
    
    # Generate content using Gemini
    response = await model.generate_content_async(system_prompt)
    
    # Extract and validate the Manim code
    manim_code = response.text
    
    # Basic validation
    if not manim_code or "import manim" not in manim_code.lower():
        raise ValueError("Failed to generate valid Manim code")
    
    return manim_code 