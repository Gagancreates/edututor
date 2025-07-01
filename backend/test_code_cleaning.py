"""
Test script for the code cleaning functionality.
"""
import re

def clean_code(code_text):
    """
    Clean the code text by removing any Markdown formatting.
    
    Args:
        code_text: The code text to clean
        
    Returns:
        Cleaned code text
    """
    # Remove Markdown code block markers (```python and ```)
    code_text = re.sub(r'^```python\s*', '', code_text, flags=re.MULTILINE)
    code_text = re.sub(r'^```\s*$', '', code_text, flags=re.MULTILINE)
    
    # Remove any other Markdown formatting that might be present
    code_text = re.sub(r'^```.*\s*', '', code_text, flags=re.MULTILINE)
    
    return code_text.strip()

def test_code_cleaning():
    """
    Test the code cleaning function with various inputs.
    """
    # Test case 1: Code with ```python and ``` markers
    test_code_1 = """```python
from manim import *

class CreateScene(Scene):
    def construct(self):
        title = Text("Hello, World!")
        self.play(Write(title))
        self.wait(2)
        self.play(FadeOut(title))
```"""
    
    # Test case 2: Code with only ``` markers
    test_code_2 = """```
from manim import *

class CreateScene(Scene):
    def construct(self):
        title = Text("Hello, World!")
        self.play(Write(title))
        self.wait(2)
        self.play(FadeOut(title))
```"""
    
    # Test case 3: Clean code without markers
    test_code_3 = """from manim import *

class CreateScene(Scene):
    def construct(self):
        title = Text("Hello, World!")
        self.play(Write(title))
        self.wait(2)
        self.play(FadeOut(title))"""
    
    # Clean the test codes
    cleaned_code_1 = clean_code(test_code_1)
    cleaned_code_2 = clean_code(test_code_2)
    cleaned_code_3 = clean_code(test_code_3)
    
    # Print the results
    print("Test Case 1 - Code with ```python and ``` markers:")
    print("Before:")
    print(test_code_1)
    print("\nAfter:")
    print(cleaned_code_1)
    print("\n" + "-" * 50 + "\n")
    
    print("Test Case 2 - Code with only ``` markers:")
    print("Before:")
    print(test_code_2)
    print("\nAfter:")
    print(cleaned_code_2)
    print("\n" + "-" * 50 + "\n")
    
    print("Test Case 3 - Clean code without markers:")
    print("Before:")
    print(test_code_3)
    print("\nAfter:")
    print(cleaned_code_3)

if __name__ == "__main__":
    test_code_cleaning() 