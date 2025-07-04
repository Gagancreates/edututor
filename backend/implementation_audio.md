# Audio Narration Implementation for EduTutor

## Overview
This document outlines the technical implementation plan for adding audio narration to our Manim-generated educational videos using the Eleven Labs API. The goal is to extract narration text from the Manim code, convert it to speech using Eleven Labs' text-to-speech service, and merge the audio with the video to create a complete educational experience.

## 1. Technical Architecture

### 1.1 System Flow
1. User submits a prompt for video generation
2. Gemini API generates Manim code
3. **NEW**: Text extraction service parses the Manim code to identify narration text
4. **NEW**: Eleven Labs API converts text to speech
5. Manim generates the animation video
6. **NEW**: FFmpeg merges the video and audio with proper synchronization
7. Final video is served to the user

### 1.2 Component Diagram
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  User Input  │───▶│  Gemini API │───▶│  Manim Code │
└─────────────┘    └─────────────┘    └──────┬──────┘
                                            │
                                            ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Final Video │◀───│   FFmpeg    │◀───│  Text       │
│  with Audio  │    │   Merger    │    │  Extraction │
└─────────────┘    └──────┬──────┘    └──────┬──────┘
                          ▲                  │
                          │                  ▼
                    ┌─────────────┐    ┌─────────────┐
                    │  Manim      │    │ Eleven Labs │
                    │  Animation  │    │     TTS     │
                    └─────────────┘    └─────────────┘
```

## 2. Implementation Details

### 2.1 New Dependencies
```
# Add to requirements.txt
elevenlabs==0.2.24
ffmpeg-python==0.2.0
pydub==0.25.1
```

### 2.2 New Files to Create

#### 2.2.1 TTS Service
**File**: `backend/app/services/tts.py`
- Handles communication with Eleven Labs API
- Converts text to speech
- Manages audio file generation and storage

#### 2.2.2 Text Extraction Service
**File**: `backend/app/services/text_extraction.py`
- Parses Manim code to extract narration text
- Identifies text that should be narrated
- Creates a script with timing information

#### 2.2.3 Audio-Video Merger
**File**: `backend/app/services/media_processing.py`
- Uses FFmpeg to merge audio and video
- Handles synchronization between audio and visuals
- Manages final video output

### 2.3 Files to Modify

#### 2.3.1 Manim Service
**File**: `backend/app/services/manim.py`
- Update to integrate with text extraction and audio generation
- Modify video generation flow to include audio processing

#### 2.3.2 Generate Router
**File**: `backend/app/routers/generate.py`
- Update to handle audio generation in the background task
- Add endpoints for audio status if needed

#### 2.3.3 Helpers
**File**: `backend/app/utils/helpers.py`
- Add utility functions for audio file management
- Update video status functions to include audio status

## 3. Text Extraction Strategy

### 3.1 Narration Text Sources
We'll extract narration text from the following sources in the Manim code:

1. **Comments**: Extract comments that describe what's happening in the scene
   ```python
   # This is a comment that could be narrated
   ```

2. **Text Objects**: Extract text from Text objects in the Manim code
   ```python
   title = Text("Introduction to Calculus")
   ```

3. **MathTex Objects**: Convert mathematical expressions to spoken form
   ```python
   equation = MathTex(r"F = ma")
   ```

### 3.2 Timing Strategy
To ensure proper synchronization between audio and video:

1. **Scene-based Timing**: Extract wait() calls to determine timing
   ```python
   self.wait(2)  # Wait for 2 seconds
   ```

2. **Animation-based Timing**: Calculate duration based on animation run_time
   ```python
   self.play(Write(text), run_time=1.5)
   ```

3. **Default Timing**: Assign default durations for narration when timing is not explicit

## 4. Eleven Labs Integration

### 4.1 API Integration
- Use Eleven Labs Python SDK for API communication
- Implement API key management through environment variables
- Select appropriate voices for educational content

### 4.2 Audio Generation Parameters
- Voice selection (default and user-customizable options)
- Speech rate and clarity settings optimized for educational content
- Audio quality settings (balancing quality vs. file size)

### 4.3 Error Handling
- Implement retry logic for API failures
- Fallback mechanisms if TTS service is unavailable
- Error reporting and logging

## 5. Audio-Video Synchronization

### 5.1 FFmpeg Integration
- Use ffmpeg-python for programmatic control of FFmpeg
- Implement precise audio-video merging with proper synchronization
- Handle different video and audio formats and codecs

### 5.2 Synchronization Methods
1. **Scene-based Synchronization**: Match audio segments to scene transitions
2. **Timestamp-based Synchronization**: Use extracted timestamps to align audio with visuals
3. **Chunk-based Processing**: Process audio in chunks that match video segments

### 5.3 Performance Optimization
- Parallel processing of audio generation and video rendering
- Caching of audio segments for reuse
- Efficient file handling to minimize disk I/O

## 6. Implementation Steps

### 6.1 Phase 1: Basic Integration
1. Set up Eleven Labs API integration
2. Implement basic text extraction from Manim code
3. Create simple audio-video merging with FFmpeg
4. Test with simple videos to verify the concept

### 6.2 Phase 2: Enhanced Synchronization
1. Improve text extraction with better timing information
2. Implement more sophisticated audio-video synchronization
3. Add support for multiple voices and speech parameters
4. Optimize performance for longer videos

### 6.3 Phase 3: User Experience Improvements
1. Add user controls for voice selection
2. Implement subtitle generation from narration text
3. Add audio quality options for different bandwidth scenarios
4. Create a feedback mechanism for audio quality improvement

## 7. Testing Strategy

### 7.1 Unit Tests
- Test text extraction from various Manim code patterns
- Verify TTS API integration with mock responses
- Test FFmpeg commands for different scenarios

### 7.2 Integration Tests
- End-to-end tests for the complete audio-video generation pipeline
- Performance testing for various video lengths and complexities
- Error handling and recovery tests

### 7.3 User Acceptance Testing
- Verify audio-video synchronization quality
- Test voice clarity and pronunciation accuracy
- Evaluate overall user experience with narrated videos

## 8. Fallback Mechanisms

### 8.1 TTS Service Unavailability
- Implement a queue system for retrying failed TTS requests
- Provide video without audio if TTS fails after multiple retries
- Notify users about audio generation status

### 8.2 Text Extraction Failures
- Implement fallback text generation if extraction fails
- Use generic narration for sections where specific text can't be extracted
- Log extraction failures for improvement

## 9. Future Enhancements

### 9.1 Advanced Features
- Multiple voice support for different characters/concepts
- Emotion and emphasis in narration based on content
- Background music and sound effects
- Interactive transcripts that highlight as the video plays

### 9.2 Performance Improvements
- Implement streaming audio generation for longer videos
- Optimize audio file sizes for different platforms
- Implement progressive loading for better user experience

## 10. Conclusion
This implementation plan provides a comprehensive approach to adding audio narration to our Manim-generated educational videos. By leveraging the Eleven Labs API for high-quality text-to-speech and implementing sophisticated text extraction and audio-video synchronization, we can create a more engaging and accessible educational experience for our users. 