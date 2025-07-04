"""
Gemini API integration for generating Manim code.
"""
import os
import logging
import traceback
import google.generativeai as genai
from typing import Optional
import asyncio
import time
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

class ManimEducationalAgent:
    """
    Advanced intelligent agent for educational content classification and 
    specialized Manim code generation optimized for mathematical concepts.
    """
    
    def __init__(self):
        self.classifiers = {
            'step_by_step_problem': ['solve', 'calculate', 'find', 'determine', 'compute', 'equation', 'step', 'value'],
            'conceptual_explanation': ['explain', 'what is', 'concept', 'understand', 'meaning', 'definition'],
            'visual_demonstration': ['show', 'demonstrate', 'visualize', 'animate', 'graph', 'plot', 'draw'],
            'formula_derivation': ['derive', 'proof', 'derivation', 'prove', 'formula', 'where does'],
            'comparison_analysis': ['compare', 'difference', 'vs', 'versus', 'contrast', 'similar'],
            'interactive_exploration': ['explore', 'investigate', 'experiment', 'what if', 'interactive']
        }
        
    def classify_and_generate(self, topic, prompt, duration_minutes=3):
        """Classifies content and generates optimized Manim code"""
        content_type = self._classify_content(prompt)
        return self._generate_specialized_code(content_type, topic, prompt, duration_minutes)
    
    def _classify_content(self, prompt):
        """Efficient content classification using keyword matching"""
        prompt_lower = prompt.lower()
        scores = {}
        
        for content_type, keywords in self.classifiers.items():
            scores[content_type] = sum(1 for keyword in keywords if keyword in prompt_lower)
        
        return max(scores, key=scores.get) if max(scores.values()) > 0 else 'conceptual_explanation'
    
    def _generate_specialized_code(self, content_type, topic, prompt, duration_minutes):
        """Generate highly optimized Manim code based on content type"""
        
        base_requirements = f"""
GENERATE PURE PYTHON CODE ONLY - NO MARKDOWN, NO EXPLANATIONS OUTSIDE CODE

CRITICAL MANIM REQUIREMENTS:
-**make sure that you dont overwrite the text from the previous scene**
-**make sure that all the text rendered does not overlap**
- from manim import * (required import)
- class CreateScene(Scene): (exact class name and inheritance)
- Complete, executable Python code only
- No external assets (images, videos, audio)
- Use only: Create, Write, FadeIn, FadeOut, Transform, ReplacementTransform animations
- Text classes: Text(), Tex(), MathTex() only
- Basic shapes: Circle, Square, Rectangle, Arrow, Line
- Always include self.wait() between animations (1-3 seconds)
- End with self.play(FadeOut(*self.mobjects))
- run_time between 0.5-2 seconds for all animations
- Avoid display_frame, ZoomedScene, TransformMatchingTex errors


COMPATIBILITY WARNINGS:
-Ensure all methods are properly called with parentheses and correct arguments, so that variables used in arithmetic are numeric values, not method objects, to avoid TypeError issues
- DO NOT use .align_left(), .align_right(), or .align_center() methods on Text objects
- For text alignment, use .to_edge(LEFT), .to_edge(RIGHT), or .move_to(ORIGIN) instead
-Do not use rotation in constructors; call .rotate() separately

TOPIC: {topic or 'Mathematics'}
CONTENT: {prompt}
DURATION: {duration_minutes} minutes

"""
        
        if content_type == 'step_by_step_problem':
            return base_requirements + """
STEP-BY-STEP PROBLEM SOLVING CODE:

Structure (optimal timing):
1. Problem Setup (20%): Present problem, highlight unknowns, show given data
2. Strategy (15%): Explain approach, show method choice reasoning  
3. Step-by-Step Solution (50%): Individual steps with clear transitions
4. Verification (15%): Check answer, interpret result

For each step:
- State action: "Step N: [action]" 
- Show math: Use MathTex for equations
- Explain reasoning: "Because..." text
- Highlight result: Colored boxes/emphasis
- Transition: "Next we..." or "This gives us..."

Mathematical Step Template:
```python
# Step presentation
step_title = Text("Step 1: [Action]", color=BLUE).to_edge(UP)
step_math = MathTex(r"equation", color=YELLOW).scale(1.2)
step_explanation = Text("We do this because...", color=WHITE).scale(0.7)

self.play(Write(step_title))
self.wait(1)
self.play(Write(step_math))
self.wait(2)
self.play(Write(step_explanation))
self.wait(2)
self.play(FadeOut(step_title, step_math, step_explanation))
```

Show all algebraic manipulations explicitly. Use proper LaTeX syntax.
"""
        
        elif content_type == 'conceptual_explanation':
            return base_requirements + """
CONCEPTUAL EXPLANATION CODE:

Structure (optimal flow):
1. Introduction (25%): Definition, importance, prior knowledge connections
2. Core Understanding (40%): Break into components, visual analogies, multiple representations
3. Examples (25%): 2-3 detailed examples, properties, misconceptions
4. Applications (10%): Real-world connections, advanced previews

Teaching Approach:
- Concrete → Abstract progression
- Multiple representations (visual, algebraic, verbal)
- Build on familiar concepts
- Visual metaphors and analogies
- Progressive complexity

Visual Development:
- Animate concept building
- Color-code different aspects  
- Use progressive revelation
- Create memorable visuals
- Show concept evolution

Mathematical Depth:
- Formal definitions + intuitive explanations
- Properties and theorems
- Concrete examples
- Theoretical foundations
"""
        
        elif content_type == 'visual_demonstration':
            return base_requirements + """
VISUAL DEMONSTRATION CODE:

Structure (dynamic focus):
1. Dynamic Visualization (45%): Animated graphs/objects, real-time transformations
2. Interactive Elements (30%): Parameter changes, cause-effect relationships
3. Multiple Perspectives (15%): Different viewpoints, various representations
4. Key Insights (10%): Visual patterns, mathematical principles

Animation Techniques:
- Create() for drawing objects
- Transform() for changes
- ValueTracker for parameters
- always_redraw for dynamic updates
- Smooth camera movements

Focus Areas:
- Function transformations
- Geometric relationships
- Statistical patterns
- Calculus concepts
- Algebraic manipulations
- Number theory patterns

Make abstract concepts tangible through compelling visual animation.
"""
        
        elif content_type == 'formula_derivation':
            return base_requirements + """
FORMULA DERIVATION CODE:

Structure (logical flow):
1. Starting Point (15%): Final formula, importance, starting assumptions
2. Logical Steps (70%): Each step justified, explicit manipulations, reasoning
3. Verification (10%): Test with examples, known cases, dimensional analysis
4. Significance (5%): Applications, implications, broader connections

Derivation Method:
- Motivate each step
- Show all assumptions
- Use proper notation
- Include justifications
- Address restrictions
- Maintain logical flow

Mathematical Rigor:
- Proper symbols and notation
- All assumptions stated
- Necessary justifications
- Domain restrictions
- Special cases addressed

Create masterclass-level mathematical reasoning demonstration.
"""
        
        elif content_type == 'comparison_analysis':
            return base_requirements + """
COMPARISON ANALYSIS CODE:

Structure (systematic approach):
1. Introduction (15%): Concepts introduced, comparison value, framework
2. Side-by-Side Analysis (55%): Simultaneous display, similarities/differences
3. Detailed Comparison (20%): When to use, advantages/disadvantages, misconceptions
4. Synthesis (10%): Key insights, method selection, connections

Visualization Techniques:
- Split-screen layouts
- Consistent color coding
- Comparison tables/charts
- Transition animations
- Visual emphasis for differences

Comparison Focus:
- Solution methods
- Similar concepts
- Mathematical evolution
- Efficiency considerations
- Approach selection

Help students understand when and why to use different approaches.
"""
        
        else:  # interactive_exploration
            return base_requirements + """
INTERACTIVE EXPLORATION CODE:

Structure (discovery-based):
1. Setup & Questions (20%): Pose questions, framework, variable parameters
2. Guided Exploration (55%): Parameter variations, pattern emergence
3. Pattern Recognition (15%): Identify patterns, general principles
4. Extensions (10%): Further exploration, broader connections

Interactive Techniques:
- ValueTracker for parameters
- Dynamic response animations
- Multiple scenarios
- always_redraw updates
- Mathematical "experiments"

Exploration Themes:
- Function parameter effects
- Geometric transformations
- Number patterns
- Optimization problems
- Probability investigations

Encourage mathematical discovery through guided visual exploration.
"""

async def generate_manim_code(
    prompt: str, 
    topic: Optional[str] = None, 
    grade_level: Optional[str] = None, 
    duration_minutes: float = 3.0,
    max_retries: int = 3,
    retry_delay: float = 2.0,
    timeout: float = 120.0
) -> str:
    """
    Generate Manim code using the Gemini API with retry logic and timeout handling.
    
    Args:
        prompt: The prompt for generating the video
        topic: The educational topic (optional)
        grade_level: The target grade level (optional, not used in current implementation)
        duration_minutes: The desired duration in minutes (default: 3.0, min: 0.67, max: 3.0)
        max_retries: Maximum number of retry attempts for API calls (default: 3)
        retry_delay: Delay between retries in seconds (default: 2.0)
        timeout: Timeout for the API call in seconds (default: 120.0)
        
    Returns:
        Generated Manim Python code
    """
    try:
        logger.info(f"Generating Manim code for prompt: {prompt}")
        
        # Check if API key is configured
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not set. Please run 'python setup_env.py' to configure.")
        
        # Ensure duration is within bounds (40 seconds to 3 minutes)
        duration_minutes = max(0.67, min(duration_minutes, 3.0))
        
        # Use the ManimEducationalAgent to generate specialized prompt
        agent = ManimEducationalAgent()
        specialized_prompt = agent.classify_and_generate(topic, prompt, duration_minutes)
        
        # Simplify prompt if it's too complex (for "neural network from scratch" type prompts)
        if "neural network" in prompt.lower() and "from scratch" in prompt.lower():
            logger.info("Detected complex 'neural network from scratch' prompt, simplifying...")
            specialized_prompt += "\n\nIMPORTANT: Focus on a simple, high-level explanation of neural networks with basic visuals. Avoid complex code and detailed implementations."
        
        # Generate the code using Gemini with retry logic
        model = genai.GenerativeModel('gemini-2.5-flash-preview-05-20')
        
        # Initialize variables for retry loop
        attempts = 0
        last_exception = None
        
        while attempts < max_retries:
            try:
                logger.info(f"API call attempt {attempts + 1}/{max_retries}")
                
                # Create a timeout for the API call
                async def api_call():
                    return model.generate_content(specialized_prompt)
                
                # Execute with timeout
                response = await asyncio.wait_for(api_call(), timeout=timeout)
                
                # If we get here, the call was successful
                if not response.text:
                    logger.error("Gemini API returned empty response")
                    raise ValueError("Failed to generate code: Empty response from Gemini API")
                
                manim_code = response.text.strip()
                logger.info(f"Generated Manim code preview: {manim_code[:500]}...")
                return manim_code
                
            except asyncio.TimeoutError:
                last_exception = asyncio.TimeoutError("API call timed out")
                logger.warning(f"API call timed out (attempt {attempts + 1}/{max_retries})")
            except Exception as e:
                last_exception = e
                logger.warning(f"API call failed with error: {str(e)} (attempt {attempts + 1}/{max_retries})")
            
            # Increment attempt counter and wait before retrying
            attempts += 1
            if attempts < max_retries:
                logger.info(f"Waiting {retry_delay} seconds before retry...")
                await asyncio.sleep(retry_delay)
                # Increase retry delay for subsequent attempts (exponential backoff)
                retry_delay *= 1.5
        
        # If we've exhausted all retries, raise the last exception
        logger.error(f"All {max_retries} API call attempts failed")
        raise last_exception or ValueError("API call failed after multiple attempts")
        
    except Exception as e:
        logger.error(f"Error generating Manim code: {str(e)}")
        logger.error(traceback.format_exc())
        raise ValueError(f"Failed to generate Manim code: {str(e)}") 