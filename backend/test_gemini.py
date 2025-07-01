"""
Test script for the Gemini API integration.
"""
import os
import asyncio
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the Gemini API client
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set")

genai.configure(api_key=GEMINI_API_KEY)

# Select the model
model = genai.GenerativeModel('gemini-2.0-flash')

async def test_gemini_api():
    """
    Test the Gemini API with a simple prompt.
    """
    prompt = "Generate a simple Python function that adds two numbers."
    
    print(f"Sending prompt to Gemini API: {prompt}")
    
    try:
        response = await model.generate_content_async(prompt)
        
        print("Response received:")
        print(response.text)
        
        print("\nTest completed successfully!")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_gemini_api()) 