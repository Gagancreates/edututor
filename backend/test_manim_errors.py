"""
Test script to verify error detection and handling for common Manim errors.
"""
import sys
from app.services.manim import check_for_common_errors

# Test cases with known errors
TEST_CASES = [
    {
        "name": "display_frame error",
        "code": """
from manim import *

class CreateScene(ZoomedScene):
    def __init__(self, **kwargs):
        super().__init__(display_frame=True, **kwargs)
    
    def construct(self):
        circle = Circle()
        self.play(Create(circle))
""",
        "should_detect": True
    },
    {
        "name": "tex_string error",
        "code": """
from manim import *

class CreateScene(Scene):
    def construct(self):
        circle = Circle()
        text = Text("Hello")
        self.play(TransformMatchingTex(circle, text))
""",
        "should_detect": True
    },
    {
        "name": "ZoomedScene usage",
        "code": """
from manim import *

class CreateScene(ZoomedScene):
    def construct(self):
        circle = Circle()
        self.play(Create(circle))
""",
        "should_detect": True
    },
    {
        "name": "ThreeDScene usage",
        "code": """
from manim import *

class CreateScene(ThreeDScene):
    def construct(self):
        sphere = Sphere()
        self.play(Create(sphere))
""",
        "should_detect": True
    },
    {
        "name": "Wrong class name",
        "code": """
from manim import *

class WrongName(Scene):
    def construct(self):
        circle = Circle()
        self.play(Create(circle))
""",
        "should_detect": True
    },
    {
        "name": "Missing import",
        "code": """
class CreateScene(Scene):
    def construct(self):
        circle = Circle()
        self.play(Create(circle))
""",
        "should_detect": True
    },
    {
        "name": "Valid code",
        "code": """
from manim import *

class CreateScene(Scene):
    def construct(self):
        # Create a circle
        circle = Circle(color=BLUE)
        self.play(Create(circle))
        self.wait(1)
        
        # Add text
        text = Text("Hello, Manim!")
        self.play(Write(text))
        self.wait(1)
        
        # Fade out
        self.play(FadeOut(circle), FadeOut(text))
""",
        "should_detect": False
    }
]

def main():
    """Run the tests"""
    print("Testing Manim error detection...\n")
    
    passed = 0
    failed = 0
    
    for test_case in TEST_CASES:
        print(f"Testing: {test_case['name']}")
        has_errors, error_message = check_for_common_errors(test_case['code'])
        
        if has_errors == test_case['should_detect']:
            print(f"✅ PASSED: {'Error correctly detected' if has_errors else 'No errors detected as expected'}")
            if has_errors:
                print(f"   Error message: {error_message}")
            passed += 1
        else:
            print(f"❌ FAILED: {'Error not detected' if test_case['should_detect'] else 'False positive error detected'}")
            if has_errors:
                print(f"   Error message: {error_message}")
            failed += 1
        
        print()
    
    print(f"Test results: {passed} passed, {failed} failed")
    return failed == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 