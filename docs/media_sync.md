# Audio-Video Synchronization Implementation Plan

## Overview

This document outlines the technical approach for improving audio-video synchronization in the EduTutor platform. The current implementation extracts text from Manim code and generates audio narration, but lacks proper timing alignment between visual elements and spoken content. This plan addresses synchronization issues through enhanced text extraction, timing-aware audio generation, and improved media processing.

## Current Implementation Analysis

### Strengths
- Successfully extracts text from Manim code
- Generates audio using Eleven Labs API
- Merges audio and video using FFmpeg

### Limitations
- Audio narration runs continuously without regard for scene timing
- No pauses or pacing adjustments for complex visualizations
- Lacks contextual narration for scenes
- No synchronization between visual elements and spoken content

## Enhanced Text Extraction

### Scene Structure Analysis

1. **Parse Manim Code Structure**
   - Identify scene classes and their inheritance hierarchy
   - Extract the `construct()` method content for each scene
   - Map animations and their durations within each scene

2. **Scene Timing Extraction**
   ```python
   def extract_scene_timings(manim_code):
       scenes = {}
       scene_pattern = r"class\s+(\w+)\(.*\):\s*(?:[^\{])*(?:def\s+construct\s*\(\s*self\s*\):\s*((?:.*?\n)+?)(?:def|\Z))"
       scene_matches = re.finditer(scene_pattern, manim_code, re.DOTALL)
       
       for match in scene_matches:
           scene_name = match.group(1)
           construct_content = match.group(2)
           
           # Extract wait times and animation durations
           wait_pattern = r"self\.wait\(([^)]*)\)"
           wait_times = re.findall(wait_pattern, construct_content)
           
           # Extract animations and estimate their durations
           animation_pattern = r"self\.play\((.*?)\)"
           animations = re.findall(animation_pattern, construct_content, re.DOTALL)
           
           scenes[scene_name] = {
               "content": construct_content,
               "wait_times": wait_times,
               "animations": animations
           }
       
       return scenes
   ```

3. **Text Element Identification**
   - Extract all text objects (Text, TextMobject, MathTex, etc.)
   - Capture text content and its appearance timing
   - Associate text with specific animations or scenes

   ```python
   def extract_text_elements(scene_content):
       text_elements = []
       
       # Match various text creation patterns
       text_patterns = [
           r"Text\(\s*[\"\'](.*?)[\"\']",
           r"TextMobject\(\s*[\"\'](.*?)[\"\']",
           r"MathTex\(\s*[\"\'](.*?)[\"\']",
           r"Tex\(\s*[\"\'](.*?)[\"\']",
           r"Title\(\s*[\"\'](.*?)[\"\']",
       ]
       
       for pattern in text_patterns:
           matches = re.findall(pattern, scene_content, re.DOTALL)
           for match in matches:
               # Clean up the extracted text
               clean_text = clean_latex_commands(match)
               
               # Try to determine when this text appears
               # (This would require more complex parsing)
               
               text_elements.append({
                   "content": clean_text,
                   "type": pattern.split("(")[0],
                   "raw": match
               })
       
       return text_elements
   ```

### Comment Extraction

1. **Structured Comment Parsing**
   - Extract docstrings and inline comments
   - Identify section markers and descriptive comments
   - Parse special comment tags for narration instructions

   ```python
   def extract_comments(manim_code):
       # Extract docstrings
       docstring_pattern = r'"""(.*?)"""'
       docstrings = re.findall(docstring_pattern, manim_code, re.DOTALL)
       
       # Extract inline comments
       inline_pattern = r'#\s*(.*?)$'
       inline_comments = re.findall(inline_pattern, manim_code, re.MULTILINE)
       
       # Look for special narration comments
       narration_pattern = r'#\s*narration:\s*(.*?)$'
       narration_comments = re.findall(narration_pattern, manim_code, re.MULTILINE)
       
       return {
           "docstrings": docstrings,
           "inline_comments": inline_comments,
           "narration_comments": narration_comments
       }
   ```

## Timing Map Generation

### Creating a Synchronized Timing Map

1. **Generate Scene Timeline**
   - Create a timeline of scenes with estimated start/end times
   - Map text elements to specific timestamps
   - Account for animations and wait times

   ```python
   def generate_timing_map(scenes):
       timing_map = []
       current_time = 0
       
       for scene_name, scene_data in scenes.items():
           scene_start = current_time
           
           # Process animations and waits in sequence
           for animation in scene_data["animations"]:
               # Estimate animation duration (simplified)
               duration = estimate_animation_duration(animation)
               current_time += duration
               
           # Add explicit wait times
           for wait in scene_data["wait_times"]:
               try:
                   wait_time = float(wait) if wait else 1.0
                   current_time += wait_time
               except ValueError:
                   # Default wait time if parsing fails
                   current_time += 1.0
           
           # Map text elements to this scene
           text_elements = extract_text_elements(scene_data["content"])
           
           timing_map.append({
               "scene": scene_name,
               "start_time": scene_start,
               "end_time": current_time,
               "duration": current_time - scene_start,
               "text_elements": text_elements
           })
       
       return timing_map
   ```

2. **Narration Point Identification**
   - Identify key points where narration should occur
   - Create markers for pauses and pace changes
   - Generate a sequence of narration segments with timing information



## Audio Generation with SSML

### Implementing Speech Synthesis Markup Language

1. **SSML Tag Integration**
   - Add `<break>` tags for pauses between segments
   - Use `<prosody>` tags to control speech rate and pitch
   - Implement `<emphasis>` for key terms

   ```python
   def add_ssml_tags(narration_text, scene_duration):
       """Add SSML tags to control pacing based on scene duration"""
       
       # Determine appropriate speech rate based on content length and scene duration
       text_length = len(narration_text.split())
       
       if text_length / scene_duration > 3.0:  # More than 3 words per second
           rate = "slow"
       elif text_length / scene_duration < 1.5:  # Less than 1.5 words per second
           rate = "medium"
       else:
           rate = "medium"
       
       # Add prosody tags for rate control
       tagged_text = f"<prosody rate='{rate}'>{narration_text}</prosody>"
       
       # Add appropriate breaks
       tagged_text += "<break time='0.8s'/>"
       
       return tagged_text
   ```

2. **Silence and Pause Management**
   - Insert strategic pauses between narration segments
   - Add longer pauses between scenes
   - Adjust pause duration based on content complexity

   ```python
   def insert_strategic_pauses(script_segments):
       """Insert strategic pauses between narration segments"""
       
       enhanced_segments = []
       
       for i, segment in enumerate(script_segments):
           # Add the segment itself
           enhanced_segments.append(segment)
           
           # Add pause after the segment if it's not the last one
           if i < len(script_segments) - 1:
               next_segment = script_segments[i + 1]
               
               # Calculate time gap to next segment
               time_gap = next_segment["time"] - segment["time"]
               
               # If there's a significant gap, add a pause
               if time_gap > 2.0:
                   pause_duration = min(time_gap / 2, 3.0)  # Cap at 3 seconds
                   enhanced_segments.append({
                       "text": f"<break time='{pause_duration}s'/>",
                       "time": segment["time"] + 0.5,
                       "type": "pause"
                   })
       
       return enhanced_segments
   ```

### Chunked Audio Generation

1. **Segment-based Audio Generation**
   - Generate audio for each narration segment separately
   - Control timing by managing chunk sizes
   - Add silence between chunks as needed

   ```python
   def generate_chunked_audio(script_segments, voice_id):
       """Generate audio in chunks for better timing control"""
       
       audio_chunks = []
       
       for segment in script_segments:
           # Generate audio for this segment
           audio_data = tts_service.generate_speech(
               text=segment["text"],
               voice_id=voice_id,
               model_id="eleven_monolingual_v1"
           )
           
           audio_chunks.append({
               "audio_data": audio_data,
               "timing": segment["time"],
               "duration": estimate_audio_duration(segment["text"]),
               "type": segment["type"]
           })
       
       return audio_chunks
   ```

2. **Audio Assembly**
   - Combine audio chunks with precise timing
   - Insert silence between chunks as needed
   - Create a single coherent audio track

## Media Processing Enhancements

### Advanced FFmpeg Integration

1. **Complex Filter Graph for Audio Alignment**
   - Use FFmpeg filter_complex for precise audio placement
   - Implement audio track segmentation to match video scenes
   - Control audio timing with adelay filters

   ```python
   def create_complex_filter(audio_chunks, video_duration):
       """Create a complex FFmpeg filter for precise audio placement"""
       
       filter_parts = []
       inputs = []
       
       # Add each audio chunk with specific delay
       for i, chunk in enumerate(audio_chunks):
           # Convert timing to milliseconds
           delay_ms = int(chunk["timing"] * 1000)
           
           # Add input for this chunk
           inputs.append(f"-i {chunk['audio_file']}")
           
           # Add adelay filter
           filter_parts.append(f"[{i}]adelay={delay_ms}|{delay_ms}[a{i}]")
       
       # Mix all delayed audio streams
       mix_inputs = "".join(f"[a{i}]" for i in range(len(audio_chunks)))
       filter_parts.append(f"{mix_inputs}amix=inputs={len(audio_chunks)}:dropout_transition=0[aout]")
       
       return " ".join(inputs), ";".join(filter_parts)
   ```

2. **Precise Audio-Video Merging**
   - Use advanced FFmpeg options for synchronization
   - Implement audio normalization for consistent volume
   - Add fade-in/fade-out effects for smooth transitions

   ```python
   def merge_audio_video_advanced(video_path, audio_chunks, output_path):
       """Merge audio and video with advanced FFmpeg options"""
       
       # Create temporary files for audio chunks
       temp_files = []
       for i, chunk in enumerate(audio_chunks):
           temp_file = f"temp/audio_chunk_{i}.mp3"
           with open(temp_file, "wb") as f:
               f.write(chunk["audio_data"])
           temp_files.append(temp_file)
       
       # Create filter complex for precise timing
       inputs, filter_complex = create_complex_filter(
           [{"audio_file": f, "timing": chunk["timing"]} 
            for f, chunk in zip(temp_files, audio_chunks)],
           get_video_duration(video_path)
       )
       
       # Build FFmpeg command
       cmd = f"ffmpeg -y -i {video_path} {inputs} -filter_complex \"{filter_complex}\" " \
             f"-map 0:v -map \"[aout]\" -c:v copy -c:a aac -b:a 192k {output_path}"
       
       # Execute command
       subprocess.run(cmd, shell=True, check=True)
       
       # Clean up temp files
       for f in temp_files:
           os.remove(f)
   ```

## Implementation Approach

### Phase 1: Enhanced Text Extraction
1. Implement scene structure analysis
2. Extract text elements with timing information
3. Parse comments and narration instructions
4. Generate initial timing map



### Phase 3: Audio Generation Enhancements
1. Implement chunked audio generation
2. Add silence and pause management
3. Test audio timing and flow
4. Optimize speech parameters

### Phase 4: Advanced Media Processing
1. Implement complex FFmpeg filter graphs
2. Test precise audio-video synchronization
3. Add audio normalization and transitions
4. Optimize for different video types

## Testing and Validation

### Synchronization Testing
1. Create test cases with various animation types
2. Measure audio-visual alignment at key points
3. Compare expected vs. actual narration timing
4. Collect user feedback on perceived synchronization

### Quality Assurance
1. Check narration relevance and educational value
2. Verify audio quality and consistency
3. Test with different video lengths and complexities
4. Ensure graceful handling of edge cases

