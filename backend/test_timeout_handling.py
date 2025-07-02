"""
Test script to verify timeout handling and retry logic in the generate_manim_code function.
"""
import asyncio
import logging
from app.services.gemini import generate_manim_code

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_generate_with_timeout():
    """
    Test the generate_manim_code function with timeout and retry logic.
    """
    try:
        # Test with a complex prompt that might cause timeouts
        prompt = "explain neural network from scratch"
        topic = "Computer Science"
        
        logger.info(f"Testing generate_manim_code with prompt: '{prompt}'")
        logger.info(f"Using timeout=60.0 seconds, max_retries=3, retry_delay=2.0 seconds")
        
        # Call the function with explicit timeout and retry parameters
        manim_code = await generate_manim_code(
            prompt=prompt,
            topic=topic,
            timeout=60.0,  # Shorter timeout for testing
            max_retries=3,
            retry_delay=2.0
        )
        
        # Check if we got a valid response
        if manim_code and "from manim import" in manim_code:
            logger.info("✅ Test passed: Successfully generated Manim code with timeout handling")
            logger.info(f"Generated code preview: {manim_code[:200]}...")
        else:
            logger.error("❌ Test failed: Generated code does not contain expected content")
            logger.error(f"Generated code: {manim_code[:200]}...")
    
    except Exception as e:
        logger.error(f"❌ Test failed with error: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())

if __name__ == "__main__":
    asyncio.run(test_generate_with_timeout()) 