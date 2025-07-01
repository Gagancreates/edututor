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

async def generate_manim_code(prompt: str, complexity: str = "medium", duration: int = 60) -> str:
    """
    Generate Manim code using Gemini API based on the educational prompt.
    
    Args:
        prompt: The user's educational prompt
        complexity: The desired complexity level (simple, medium, complex)
        duration: Target duration in seconds
        
    Returns:
        Generated Manim code as a string
    """
    # Craft the prompt for Gemini
    system_prompt = f"""
    You are an expert educational content creator specializing in creating Manim animations.
    
    Your task is to create Python code using the Manim library that will generate an educational
    video explaining the concept: "{prompt}".
    
    Requirements:
    - Complexity level: {complexity}
    - Target duration: approximately {duration} seconds
    - The code should be complete, runnable, and self-contained
    - Use Manim's Scene class and appropriate animations
    - Include clear, step-by-step explanations through text and visuals
    - Focus on educational clarity and visual engagement
    - Include appropriate mathematical notation where relevant
    - The code should be optimized to run without errors
    
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