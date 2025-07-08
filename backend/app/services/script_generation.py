import os
import logging
import json
import asyncio
import time
import google.generativeai as genai
from typing import List, Dict, Any, Optional

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the prompt template directly in the code
SCRIPT_PROMPT_TEMPLATE = """
# MANIM SCRIPT GENERATOR

Analyze Manim code and generate synchronized TTS script in JSON format.

## REQUIREMENTS
- Analyze all animations, text objects, and timing
- Create narration explaining each visual element as it appears
- Generate precise timing matching video animations
- Convert math expressions to spoken form
- Ensure educational flow with appropriate pauses

## JSON FORMAT
Each script segment contains:
- `"text"`: Exact text to speak (or "[PAUSE]" for silence)
- `"timing"`: Object with `"start"` (float) and `"duration"` (float) in seconds
- `"type"`: "introduction", "section_title", "narration", "equation", "explanation", "transition", "pause", "conclusion"
- `"math_expression"`: (optional) Original LaTeX if applicable
- `"emphasis"`: (optional) "high", "medium", "low" for TTS emphasis

## TIMING RULES
1. Track cumulative time from video start
2. For animations: start_time = current_time, duration = run_time
3. For wait(): add wait time to current_time
4. Allow reading time based on text length and mathematical complexity

## MATH CONVERSION
- x^2/x^3 → "x squared/cubed"
- x^n → "x to the power of n"
- √x → "square root of x"
- ∫/∑ → "integral of/sum of"
- +/-/×/÷ → "plus/minus/times/divided by"
- =/≠ → "equals/not equal to"
- </>/≤/≥ → "less than/greater than/less than or equal to/greater than or equal to"
- π/θ/∞ → "pi/theta/infinity"
- \frac{a}{b} → "a over b"
- (a+b) → "open parenthesis a plus b close parenthesis"

## NARRATION STYLE
- Clear, concise educational tone
- Use transitions: "Now let's", "Next we'll", "Notice that"
- Provide context before complex concepts
- Include verification: "As we can see", "This shows us"
- Active voice with natural pauses

## PAUSE TIMING
- 0.3s: Speech breaks | 0.5s: Related concepts | 1.0s: New sections | 1.5s: Complex equations | 2.0s: Major transitions

## EXAMPLE OUTPUT
```json
[
  {
    "text": "Welcome to today's lesson on quadratic equations",
    "timing": {
      "start": 0.0,
      "duration": 3.5
    },
    "type": "introduction",
    "emphasis": "medium"
  },
  {
    "text": "[PAUSE]",
    "timing": {
      "start": 3.5,
      "duration": 0.5
    },
    "type": "pause"
  },
  {
    "text": "The general form is ax squared plus bx plus c equals zero",
    "timing": {
      "start": 4.0,
      "duration": 4.5
    },
    "type": "equation",
    "math_expression": "ax^2 + bx + c = 0",
    "emphasis": "high"
  }
]
```

## QUALITY REQUIREMENTS
- Total script duration must match video duration
- No gaps or overlaps in timing
- Natural speech rhythm with appropriate pauses
- Educational value in every segment
- Mathematical accuracy in spoken form

"""

async def generate_script_from_manim_code(
    video_id: str,
    manim_code: str,
    prompt: str,
    topic: Optional[str] = None,
    max_retries: int = 3,
    retry_delay: float = 5.0,
    timeout: float = 300.0  # 5 minutes timeout
) -> List[Dict[str, Any]]:
    """
    Generate a synchronized script for a Manim video using Gemini.
    
    Args:
        video_id: The ID of the video
        manim_code: The Manim code for which to generate a script
        prompt: The original prompt used to generate the Manim code
        topic: The educational topic (optional)
        max_retries: Maximum number of retries on failure
        retry_delay: Delay between retries in seconds
        timeout: Timeout for the API call in seconds
        
    Returns:
        List of script segments with text and timing information
    """
    retries = 0
    last_exception = None
    
    while retries <= max_retries:
        try:
            logger.info(f"Generating script for video ID: {video_id} (attempt {retries + 1}/{max_retries + 1})")
            
            # Use the hardcoded prompt template
            script_prompt = SCRIPT_PROMPT_TEMPLATE.replace("[MANIM_CODE_HERE]", manim_code)
            
            # Add context about the original prompt and topic
            script_prompt = script_prompt.replace(
                "GENERATE SYNCHRONIZED SCRIPT FROM MANIM CODE", 
                f"GENERATE SYNCHRONIZED SCRIPT FROM MANIM CODE\nORIGINAL PROMPT: {prompt}\nTOPIC: {topic or 'Educational content'}"
            )
            
            # Configure Gemini API
            GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
            if not GEMINI_API_KEY:
                raise ValueError("GEMINI_API_KEY not set in environment variables")
                
            genai.configure(api_key=GEMINI_API_KEY)
            
            # Use a more capable model for script generation
            model = genai.GenerativeModel('gemini-2.5-flash-preview-05-20')
            
            # Generate the script with timeout
            try:
                # Create a task with timeout
                response_task = asyncio.create_task(
                    asyncio.to_thread(
                        model.generate_content,
                        script_prompt,
                        generation_config={"temperature": 0.2}  # Lower temperature for more precise output
                    )
                )
                response = await asyncio.wait_for(response_task, timeout=timeout)
            except asyncio.TimeoutError:
                logger.warning(f"API call timed out after {timeout} seconds")
                raise TimeoutError(f"API call timed out after {timeout} seconds")
            
            if not response.text:
                raise ValueError("Empty response from Gemini API")
            
            # Extract the JSON script from the response
            script_text = response.text
            
            # Clean up the response text to extract only the JSON part
            if "```json" in script_text:
                script_text = script_text.split("```json")[1].split("```")[0].strip()
            elif "```" in script_text:
                script_text = script_text.split("```")[1].strip()
            
            # Parse the JSON script
            script = json.loads(script_text)
            
            # Save the script to the video directory
            script_path = os.path.join("videos", video_id, "script.json")
            os.makedirs(os.path.dirname(script_path), exist_ok=True)
            with open(script_path, "w") as f:
                json.dump(script, f, indent=2)
            
            logger.info(f"Successfully generated script for video ID: {video_id}")
            return script
            
        except Exception as e:
            last_exception = e
            retries += 1
            logger.warning(f"Error generating script (attempt {retries}/{max_retries + 1}): {str(e)}")
            
            if retries <= max_retries:
                # Wait before retrying
                logger.info(f"Retrying in {retry_delay} seconds...")
                await asyncio.sleep(retry_delay)
                # Increase delay for next retry (exponential backoff)
                retry_delay *= 1.5
            else:
                logger.error(f"Failed to generate script after {max_retries + 1} attempts: {str(e)}")
                break
    
    # If we've exhausted all retries, raise the last exception
    raise ValueError(f"Failed to generate script: {str(last_exception)}") 