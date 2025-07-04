# Audio Narration Feature for EduTutor

This document provides information about the audio narration feature for EduTutor, which adds voice narration to Manim-generated educational videos.

## Overview

The audio narration feature extracts text from Manim code, converts it to speech using the Eleven Labs API, and merges the audio with the video to create a complete educational experience.

## Setup

### Prerequisites

- Python 3.8+
- FFmpeg installed on your system
- Eleven Labs API key

### Installation

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

2. Set up your environment variables:

```bash
python setup_env.py
```

This will prompt you to enter your Eleven Labs API key.

## How It Works

### 1. Text Extraction

The system extracts narration text from Manim code using the following sources:

- Section comments (e.g., `# 1. Introduction`)
- Text objects (e.g., `Text("Introduction to Calculus")`)
- General comments

### 2. Text-to-Speech

The extracted text is converted to speech using the Eleven Labs API, which provides high-quality, natural-sounding voices.

### 3. Audio-Video Merging

The generated audio is merged with the Manim-generated video using FFmpeg to create a final video with narration.

## Components

### Text Extraction Service

`backend/app/services/text_extraction.py` - Parses Manim code to extract narration text and timing information.

### TTS Service

`backend/app/services/tts.py` - Handles communication with the Eleven Labs API to convert text to speech.

### Media Processing Service

`backend/app/services/media_processing.py` - Uses FFmpeg to merge audio and video files.

## Testing

You can test the audio narration feature using the provided test script:

```bash
python test_audio_narration.py
```

This will:
1. Extract text from a sample Manim code
2. Convert the text to speech
3. Generate audio for the extracted script

## Troubleshooting

### No Audio in Generated Videos

- Check that your Eleven Labs API key is set correctly
- Verify that FFmpeg is installed and accessible in your PATH
- Check the logs for any errors during audio generation or merging

### Poor Audio Quality

- Try different voice settings in the TTS service
- Ensure the extracted text is properly formatted
- Check the audio files generated in the `audio` directory

## Future Enhancements

- Support for multiple voices
- More sophisticated audio-video synchronization
- Interactive transcripts
- Background music and sound effects 