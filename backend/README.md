# EduTutor Backend

This is the backend service for EduTutor, an educational video generation platform.

## Features

- Generate educational videos using Manim based on text prompts
- AI-powered content generation with Google Gemini
- Voice narration with ElevenLabs TTS
- RESTful API for frontend integration

## Setup

### Prerequisites

- Python 3.8 or higher
- FFmpeg (for audio-video processing)

### Installation

1. Clone the repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set up environment variables:

```bash
python setup_env.py
```

This will prompt you to enter your Google Gemini API key and ElevenLabs API key.

### API Keys

- **Google Gemini API Key**: Required for generating educational content. Get it from [Google AI Studio](https://aistudio.google.com/app/apikey).
- **ElevenLabs API Key**: Required for voice narration. Get it from [ElevenLabs](https://elevenlabs.io/app/api-key).

## Running the Server

```bash
cd backend
uvicorn app.main:app --reload
```

The server will start on http://localhost:8000.

## API Endpoints

### Generate Video

```
POST /api/generate
```

Request body:
```json
{
  "prompt": "Explain the concept of gravity",
  "topic": "Physics",
  "grade_level": "High School",
  "duration_minutes": 3.0,
  "enable_narration": true,
  "voice_id": "EXAVITQu4vr4xnSDxMaL"
}
```

Response:
```json
{
  "video_id": "12345678-1234-5678-1234-567812345678",
  "status": "processing"
}
```

### Get Video Status

```
GET /api/video/{video_id}/status
```

Response:
```json
{
  "video_id": "12345678-1234-5678-1234-567812345678",
  "status": "completed",
  "message": "Video generation completed with narration",
  "video_url": "/api/video/12345678-1234-5678-1234-567812345678",
  "has_narration": true
}
```

### Get Video

```
GET /api/video/{video_id}
```

Returns the video file.

### List Available Voices

```
GET /api/voices
```

Response:
```json
{
  "voices": [
    {
      "voice_id": "EXAVITQu4vr4xnSDxMaL",
      "name": "Rachel",
      "description": "A warm and professional female voice",
      "preview_url": "https://example.com/preview.mp3",
      "category": "professional"
    },
    ...
  ]
}
```

## Voice Narration

The system can automatically generate voice narration for educational videos using ElevenLabs' text-to-speech technology. The narration is extracted from the text content in the Manim code and synchronized with the video.

To enable narration:
1. Set `enable_narration` to `true` in your API request
2. Optionally specify a `voice_id` (use the `/api/voices` endpoint to get available voices)
3. Make sure you have set up your ElevenLabs API key

## License

This project is licensed under the MIT License - see the LICENSE file for details. 