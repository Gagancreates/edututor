import requests
import json
import time
import os
from pathlib import Path

# Test configuration
BASE_URL = "http://localhost:8000"
VIDEO_ID = "test_video_status"

def test_video_status_during_audio_processing():
    """Test that the video status API works correctly during audio processing."""
    
    # Create test directories
    videos_dir = Path("./videos")
    video_dir = videos_dir / VIDEO_ID
    video_dir.mkdir(parents=True, exist_ok=True)
    
    # Create a test video file
    test_video_path = video_dir / f"{VIDEO_ID}.mp4"
    if not test_video_path.exists():
        with open(test_video_path, "wb") as f:
            # Create an empty MP4 file
            f.write(b"")
    
    # Create audio processing marker
    marker_path = video_dir / "audio_processing.marker"
    with open(marker_path, "w") as f:
        f.write("Audio narration processing in progress")
    
    try:
        # Test 1: Check video status endpoint
        print("Testing video status endpoint...")
        status_response = requests.get(f"{BASE_URL}/api/video/{VIDEO_ID}/status")
        status_data = status_response.json()
        
        print(f"Status response: {json.dumps(status_data, indent=2)}")
        assert status_response.status_code == 200, f"Expected status code 200, got {status_response.status_code}"
        assert status_data["status"] == "processing", f"Expected status 'processing', got {status_data['status']}"
        assert "video_url" in status_data, "Expected video_url in status response"
        
        # Test 2: Check video endpoint (should return status response)
        print("\nTesting video endpoint...")
        video_response = requests.get(f"{BASE_URL}/api/video/{VIDEO_ID}")
        
        print(f"Video response status code: {video_response.status_code}")
        assert video_response.status_code == 202, f"Expected status code 202, got {video_response.status_code}"
        
        video_data = video_response.json()
        print(f"Video response: {json.dumps(video_data, indent=2)}")
        assert video_data["status"] == "processing", f"Expected status 'processing', got {video_data['status']}"
        
        print("\nAll tests passed!")
        
    finally:
        # Clean up
        if marker_path.exists():
            marker_path.unlink()
        
        # Uncomment to clean up test video
        # if test_video_path.exists():
        #     test_video_path.unlink()
        # if video_dir.exists():
        #     video_dir.rmdir()

if __name__ == "__main__":
    test_video_status_during_audio_processing()