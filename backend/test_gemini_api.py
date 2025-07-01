"""
Test script to verify Gemini API configuration.
"""
import os
import google.generativeai as genai
from dotenv import load_dotenv

def test_gemini_api():
    """
    Test if the Gemini API key is properly configured.
    """
    print("Testing Gemini API configuration...")
    
    # Load environment variables from .env file
    load_dotenv()
    
    # Check if API key is set
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY not found in environment variables")
        print("Please run 'python setup_env.py' to set up your API key")
        return False
    
    print(f"Found API key: {api_key[:4]}...{api_key[-4:]}")
    
    try:
        # Configure the API
        genai.configure(api_key=api_key)
        
        # Create a simple test prompt
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content("Hello, please respond with 'API is working correctly'")
        
        # Check the response
        if response.text:
            print(f"API response: {response.text}")
            print("\nGemini API is configured correctly!")
            return True
        else:
            print("ERROR: Received empty response from Gemini API")
            return False
    
    except Exception as e:
        print(f"ERROR: Failed to connect to Gemini API: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_gemini_api()
    if not success:
        print("\nPlease make sure:")
        print("1. You have a valid Gemini API key")
        print("2. The API key is correctly set in the .env file")
        print("3. You have an active internet connection")
        print("\nRun 'python setup_env.py' to reconfigure your API key") 