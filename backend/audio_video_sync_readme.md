# Audio-Video Synchronization for EduTutor

This module provides advanced audio-video synchronization capabilities for the EduTutor platform, allowing for precise timing of narration with educational video content.

## Features

- **Enhanced Text Extraction**: Extracts narration text from Manim code with precise timing information
- **Timing Map Generation**: Creates a synchronization map between video elements and narration
- **SSML Integration**: Adds Speech Synthesis Markup Language tags for better pacing and timing
- **Advanced Media Processing**: Uses FFmpeg for precise audio placement and synchronization

## Components

### Text Extraction Service

The text extraction service (`text_extraction.py`) analyzes Manim code to extract:

- Scene structure and timing
- Narration comments with precise timing
- Animation durations and wait times

### Synchronization Module

The synchronization module (`sync.py`) provides:

- Timing map generation between video elements and narration
- SSML enhancement for better speech pacing
- Strategic pause insertion

### TTS Service

The TTS service (`tts.py`) handles:

- SSML tag integration for timing control
- Silence and pause management
- Chunked audio generation

### Media Processing Service

The media processing service (`media_processing.py`) implements:

- Advanced FFmpeg integration with complex filter graphs
- Precise audio placement based on timing information
- Audio-video synchronization

## Usage

### Testing

Run the test script to verify the implementation:

```bash
python test_audio_sync.py
```

This script tests:
- Text extraction from Manim code
- Sync map generation
- SSML enhancement
- Audio generation (using dummy audio if no API key is available)
- Audio-video synchronization

### Environment Setup

Set up the environment for testing:

```bash
python setup_test_env.py
```

This script:
- Checks for required environment variables
- Creates necessary directories
- Sets default paths

## Dependencies

- FFmpeg: Required for audio-video processing
- Python packages:
  - ffmpeg-python
  - wave (for dummy audio generation)
  - elevenlabs (for production TTS)

## Implementation Details

### Timing Extraction

Timing information is extracted from Manim code by analyzing:
- `self.play()` calls and their duration
- `self.wait()` calls and their duration
- Animation sequences and their timing

### Audio Synchronization

Audio is synchronized with video using:
1. Extraction of timing information from Manim code
2. Generation of a timing map
3. Enhancement of narration text with SSML tags
4. Generation of audio segments with precise timing
5. Merging of audio segments with video using FFmpeg

### Error Handling

The implementation includes robust error handling:
- Graceful fallback to dummy audio if TTS service is unavailable
- Handling of missing FFmpeg
- Recovery from synchronization failures

## Future Improvements

- Real-time synchronization feedback
- Visual indicators for narration timing
- Interactive timing adjustment
- Support for multiple narration tracks 