SECOND_API_CALL_PROMPT = """
GENERATE SYNCHRONIZED SCRIPT FROM MANIM CODE

You are given a Manim code that creates an educational video. Your task is to analyze the code and generate a perfectly synchronized script in JSON format that will be used for text-to-speech (TTS) audio generation.

CRITICAL REQUIREMENTS:
1. Analyze every animation, text object, and timing in the Manim code
2. Create narration that explains each visual element as it appears
3. Generate precise timing that matches the video animations
4. Include appropriate pauses for comprehension
5. Convert mathematical expressions to spoken form
6. Ensure educational flow and clarity

SCRIPT FORMAT:
Generate a JSON array where each object represents a script segment with:
- "text": The exact text to be spoken (or "[PAUSE]" for silence)
- "timing": Object with "start" (float) and "duration" (float) in seconds
- "type": One of: "introduction", "section_title", "narration", "equation", "explanation", "transition", "pause", "conclusion"
- "math_expression": (optional) Original LaTeX if applicable
- "emphasis": (optional) "high", "medium", "low" for TTS emphasis

TIMING CALCULATION RULES:
1. Track cumulative time from start of video
2. For each animation: start_time = current_time, duration = run_time
3. For each wait(): add wait time to current_time
4. For text explanations: allow reading time based on text length
5. For equations: allow extra time for mathematical complexity
6. Add natural pauses between concepts

MATHEMATICAL EXPRESSION CONVERSION:
- x^2 → "x squared"
- x^3 → "x cubed"
- x^n → "x to the power of n" 
- √x → "square root of x"
- ∫ → "integral of"
- ∑ → "sum of"
- + → "plus"
- - → "minus"
- × → "times"
- ÷ → "divided by"
- = → "equals"
- ≠ → "not equal to"
- < → "less than"
- > → "greater than"
- ≤ → "less than or equal to"
- ≥ → "greater than or equal to"
- π → "pi"
- θ → "theta"
- ∞ → "infinity"
- \frac{a}{b} → "a over b"
- (a+b) → "open parenthesis a plus b close parenthesis"

NARRATION GUIDELINES:
- Keep sentences clear and concise
- Use educational tone appropriate for target audience
- Include transitional phrases: "Now let's", "Next we'll", "Notice that"
- Provide context before complex concepts
- Add verification: "As we can see", "This shows us"
- Include summary statements
- Use active voice

PAUSE STRATEGY:
- 0.5s pause: Between related concepts
- 1.0s pause: Before new sections
- 1.5s pause: After complex equations
- 2.0s pause: Major transitions
- 0.3s pause: Natural speech breaks

EXAMPLE OUTPUT FORMAT:
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

QUALITY REQUIREMENTS:
- Total script duration must match video duration
- No gaps or overlaps in timing
- Natural speech rhythm with appropriate pauses
- Educational value in every narration segment
- Mathematical accuracy in spoken form
- Logical flow from concept to concept

Here is the Manim code to analyze:
[MANIM_CODE_HERE]

Generate the synchronized script in JSON format:
"""