"""
Test script to verify Unicode error handling in the manim.py file.
"""
import os
import sys
import logging
import asyncio
import subprocess
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add the current directory to the path so we can import app modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.manim import execute_manim_code

# Test Manim code with potential Unicode issues
TEST_MANIM_CODE = """
from manim import *

class CreateScene(Scene):
    def construct(self):
        # Create a title with potential Unicode characters
        title = Text("Neural Networks Explained", font_size=48)
        title.to_edge(UP)
        
        # Create some complex mathematical equations with symbols
        eq1 = MathTex(r"f(x) = \\frac{1}{1 + e^{-x}}")
        eq2 = MathTex(r"\\nabla_{\\theta} J(\\theta) = \\frac{1}{m} \\sum_{i=1}^{m} (h_\\theta(x^{(i)}) - y^{(i)}) x^{(i)}")
        
        # Create a neural network diagram
        network = VGroup()
        layers = [3, 4, 4, 2]  # Number of neurons in each layer
        
        # Create neurons for each layer
        neurons = []
        for i, layer_size in enumerate(layers):
            layer_neurons = VGroup()
            for j in range(layer_size):
                neuron = Circle(radius=0.2, color=BLUE)
                neuron.move_to([i*2, (j - (layer_size-1)/2)*0.8, 0])
                layer_neurons.add(neuron)
            neurons.append(layer_neurons)
            network.add(layer_neurons)
        
        # Create connections between neurons
        connections = VGroup()
        for i in range(len(layers)-1):
            for neuron1 in neurons[i]:
                for neuron2 in neurons[i+1]:
                    connection = Line(neuron1.get_center(), neuron2.get_center(), stroke_width=1)
                    connections.add(connection)
        network.add(connections)
        
        # Animation sequence
        self.play(Write(title))
        self.wait(1)
        
        self.play(Create(network))
        self.wait(2)
        
        self.play(network.animate.shift(DOWN*2))
        self.wait(1)
        
        self.play(Write(eq1))
        self.wait(2)
        
        self.play(ReplacementTransform(eq1, eq2))
        self.wait(2)
        
        self.play(FadeOut(network), FadeOut(eq2), FadeOut(title))
        self.wait(1)
"""

async def test_unicode_handling():
    """
    Test the Unicode error handling in the execute_manim_code function.
    """
    video_id = "test_unicode_handling"
    
    # Make sure the video directory doesn't exist
    videos_dir = Path("./videos")
    video_dir = videos_dir / video_id
    if video_dir.exists():
        import shutil
        shutil.rmtree(video_dir)
    
    logger.info("Testing Unicode error handling in execute_manim_code...")
    
    try:
        # Execute the Manim code
        result = await execute_manim_code(video_id, TEST_MANIM_CODE)
        
        logger.info(f"Manim execution completed successfully: {result}")
        
        # Check if the video file exists
        if os.path.exists(result):
            logger.info(f"✅ Video file exists at: {result}")
            logger.info(f"Video file size: {os.path.getsize(result)} bytes")
        else:
            logger.error(f"❌ Video file not found at: {result}")
        
    except Exception as e:
        logger.error(f"❌ Test failed with error: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        
        # Check if the error file exists
        error_file = video_dir / "error.txt"
        if error_file.exists():
            with open(error_file, "r", encoding="utf-8", errors="replace") as f:
                error_content = f.read()
            logger.info(f"Error file content:\n{error_content}")
    
    # Check for stdout and stderr files
    stdout_file = video_dir / "stdout.txt"
    if stdout_file.exists():
        logger.info(f"stdout file exists: {stdout_file}")
    
    stderr_file = video_dir / "stderr.txt"
    if stderr_file.exists():
        logger.info(f"stderr file exists: {stderr_file}")
    
    logger.info("Test completed")

if __name__ == "__main__":
    asyncio.run(test_unicode_handling()) 