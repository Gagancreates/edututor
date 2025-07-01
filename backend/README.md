# EduTutor Backend

This is the backend service for EduTutor, an educational video generation platform that uses Manim to create engaging educational content.

## Setup Instructions

### Prerequisites

- Python 3.10 or higher
- FFmpeg (required by Manim for video generation)
- Gemini API key (get one from https://aistudio.google.com/app/apikey)

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/edututor.git
   cd edututor/backend
   ```

2. Create a virtual environment:
   ```
   python -m venv .venv
   ```

3. Activate the virtual environment:
   - Windows:
     ```
     .\.venv\Scripts\activate
     ```
   - Linux/Mac:
     ```
     source .venv/bin/activate
     ```

4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Set up environment variables:
   ```
   python setup_env.py
   ```
   This will prompt you to enter your Gemini API key.

6. Test the Gemini API configuration:
   ```
   python test_gemini_api.py
   ```

### Running the Server

Start the FastAPI server:
```
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000

### API Endpoints

- `GET /`: Root endpoint
- `GET /api/health`: Health check endpoint
- `POST /api/generate`: Generate a new educational video
- `GET /api/video/{video_id}`: Get a generated video
- `GET /api/video/{video_id}/status`: Check the status of a video generation

### Testing

Run the test scripts to verify different components:

- Test Manim video generation:
  ```
  python test_manim_video.py
  ```

- Test code cleaning functionality:
  ```
  python test_code_cleaning.py
  ```

- Test Gemini API:
  ```
  python test_gemini.py
  ```

- Test API endpoints:
  ```
  python test_api.py
  ```

## Troubleshooting

### Video Generation Issues

If videos are not being generated correctly:

1. Check the error logs in the `videos/{video_id}/error.txt` file
2. Verify that FFmpeg is installed and accessible in your PATH
3. Make sure Manim is installed correctly: `pip install manim`
4. Run the test script: `python test_manim_video.py`

### API Key Issues

If you're having issues with the Gemini API:

1. Verify your API key is correct
2. Run `python setup_env.py` to reconfigure your API key
3. Test the API configuration with `python test_gemini_api.py` 