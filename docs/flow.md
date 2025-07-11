# EduTutor Application Flow

## 1. Project Overview

EduTutor is a web application designed to automatically generate educational videos. Users provide a prompt, topic, and grade level, and the system uses a combination of AI services (Google's Gemini for code generation, Eleven Labs for text-to-speech) and the Manim animation engine to produce a narrated video explaining the concept.

## 2. Architecture

The application follows a standard client-server architecture:

*   **Frontend:** A Next.js application responsible for the user interface. It provides a form for users to submit video requests and a player to view the generated videos.
*   **Backend:** A Python FastAPI application that orchestrates the entire video generation pipeline. It exposes a set of REST APIs that the frontend consumes.

---

## 3. Backend Flow (Detailed)

The backend is where the core logic resides. The process is almost entirely asynchronous, relying on background tasks to handle the long-running process of video generation.

### Request Entry Point (`main.py`)

*   All incoming requests are handled by a FastAPI application defined in `app/main.py`.
*   It configures CORS to allow requests from any origin.
*   It includes the main router from `app/routers/generate.py`.
*   It defines several key endpoints:
    *   `/api/health`: A simple health check.
    *   `/api/video/{video_id}`: The primary endpoint for fetching a finished video. It can return the video file, or if the video is still being processed, it returns a `202 Accepted` status with a message indicating what's happening (e.g., "Video generation in progress" or "Adding audio narration to video").
    *   `/api/video/{video_id}/status`: An endpoint to get a JSON object representing the detailed status of the video generation process.

### Video Generation Request (`routers/generate.py`)

The main workflow is initiated by a `POST` request to `/api/generate`.

1.  **Request:** The frontend sends a JSON object with a `prompt`, `topic`, `grade_level`, and `duration_minutes`.
2.  **Task Initiation:** The endpoint receives the request, generates a unique `video_id` (UUID), and immediately queues a background task (`generate_video_task`) to handle the actual work.
3.  **Immediate Response:** It instantly returns a `202 Accepted` response to the frontend with the `video_id` and a `status` of "processing". This asynchronous pattern prevents the frontend from timing out while waiting for the long generation process.

### The Video Generation Pipeline

The `generate_video_task` kicks off a multi-step pipeline, with each step handled by a dedicated service.

#### Step 1: Code Generation (`services/gemini.py`)

This service is responsible for converting the user's natural language prompt into executable Manim Python code.

1.  **Agent-Based Prompt Engineering:** The service uses a sophisticated `ManimEducationalAgent` class. This agent first classifies the user's prompt into a category (e.g., `step_by_step_problem`, `conceptual_explanation`) based on keywords.
2.  **Specialized Prompts:** Based on the classification, it constructs a highly detailed and specialized prompt for the Google Gemini API. This prompt includes a base set of strict rules and constraints (e.g., use specific Manim classes, avoid common errors, name the class `CreateScene`) and then appends a template tailored to the content type. This is the "secret sauce" for generating high-quality, executable code.
3.  **API Call:** It calls the Gemini API with the generated prompt. The call is wrapped in a robust retry mechanism with exponential backoff and a timeout to handle API failures or delays gracefully.
4.  **Output:** The raw Python code text generated by Gemini.

#### Step 2: Narration Script Generation (`services/text_extraction.py` & `services/sync.py`)

This is the most complex and heuristic-driven part of the pipeline. The goal is to create a timed script for the narrator from the Manim code. This process happens *before* the video is rendered.

1.  **Code Parsing (`text_extraction.py`):**
    *   The `ManimTextExtractor` class uses a large set of **regular expressions** to parse the Manim code. (Note: It imports Python's `ast` module but does not use it).
    *   It extracts all `Text`, `MathTex`, `self.play`, and `self.wait` calls, as well as specially formatted comments (`# narration:`, `# section:`).

2.  **Narration Source Hierarchy (`text_extraction.py`):** The extractor uses a priority system to decide what text to use for narration:
    *   **Priority 1:** Explicit `# narration:` comments.
    *   **Priority 2:** `# section:` comments.
    *   **Priority 3:** A `# narration:` comment immediately preceding a `self.play()` call.
    *   **Priority 4:** The content of `Text()` or `MathTex()` objects inside a `self.play()` call.
    *   **Fallback:** If all else fails, it finds all text objects defined anywhere in the code.

3.  **Timing Estimation (`sync.py`):**
    *   The `SyncManager` class estimates the total duration of the video by adding up the `run_time` of `self.play` calls and the duration of `self.wait` calls.
    *   **BUG/WEAKNESS:** For the highest priority narration sources (general `# narration:` and `# section:` comments), it uses a simple heuristic: it divides the total estimated scene time evenly among the comments. This can lead to narration that is significantly out of sync with the actual animations on screen.
    *   For narration tied directly to a `self.play` call, the timing is much more accurate as it's linked to the animation's `run_time`.

4.  **Script Creation (`sync.py`):** The service consolidates this information into a list of script segments, each with a `text`, `start` time, and `duration`.

#### Step 3: Video Rendering (`services/manim.py`)

This service takes the Gemini-generated code and executes it to create a silent video file.

1.  **Pre-flight Checks:** Before running the code, it's checked against a list of common Manim errors using regex, preventing the system from wasting time on code that is known to be faulty.
2.  **Execution:** It uses Python's `subprocess` module to invoke the `manim` command-line tool in a separate process. This is wrapped in a 10-minute timeout to prevent runaway processes.
3.  **File Handling:** The Manim process runs in a temporary directory. If successful, the final `.mp4` video file is copied to a persistent location (`/videos/{video_id}/{video_id}.mp4`).
4.  **Error Handling:** All output from the Manim process (`stdout` and `stderr`) is captured. If the process fails or times out, the error is written to an `error.txt` file in the video's directory, which can be retrieved by the frontend for debugging.

#### Step 4: Text-to-Speech (`services/tts.py`)

This service converts the narration script from Step 2 into audio files.

1.  **Script Enhancement:** It takes the script and inserts strategic pauses by adding SSML `<break>` tags into the text where there are gaps in the timing.
2.  **Chunked Generation:** It processes the script segment by segment. For each piece of text, it calls the Eleven Labs API to generate an MP3 audio file. This is done asynchronously.
3.  **File Organization:** All audio segments for a video are stored in a dedicated directory (`/audio/{video_id}/`).
4.  **Manifest Creation:** After all audio chunks are generated, the service creates a `manifest.json` file. This file contains a list of all the generated audio segments, their corresponding text, and their timing information. This manifest is the key input for the final step.

#### Step 5: Audio/Video Merging (`services/media_processing.py`)

This is the final step, where the silent video and the narration audio are combined.

1.  **Entry Point:** The main `process_video_with_narration` function is called. It receives the path to the silent video and the audio manifest from the TTS service.
2.  **Complex Filter Method:** It uses the `merge_audio_segments_with_video_direct` function. This function constructs a complex `ffmpeg` command.
3.  **FFmpeg Execution:**
    *   It uses `ffmpeg`'s powerful `-filter_complex` flag.
    *   Each audio segment from the manifest is added as a separate input.
    *   An `adelay` filter is applied to each audio input, using the `start` time from the manifest to ensure each audio clip begins at the correct moment.
    *   An `amix` filter is then used to combine all the delayed audio streams into a single audio track.
    *   The original video stream is copied without re-encoding (`-c:v copy`), and the new, combined audio track is encoded, resulting in the final narrated video.
4.  **Output:** The final video is saved as `{video_id}_with_audio.mp4`.

---

## 4. Frontend Flow (High-Level)

The frontend is a Next.js application that provides the user interface for interacting with the backend.

*   **Main Page (`app/page.tsx`):** Contains the main landing page with a hero section and features. The user can input their prompt here.
*   **Generate API Route (`app/api/generate_manim/route.ts`):** When the user submits the form, the frontend doesn't call the backend directly. It calls its own API route, which then forwards the request to the Python backend. This is a common pattern in Next.js to avoid exposing backend details directly to the client and to handle environment variables securely.
*   **Video Page (`app/video/[id]/page.tsx`):**
    *   After submitting a request, the user is redirected to this page.
    *   This page periodically polls the backend's `/api/video/{video_id}/status` endpoint.
    *   It displays status messages to the user ("Generating code...", "Rendering video...", "Adding narration...").
    *   Once the status endpoint reports "completed", it shows the final video in an HTML5 `<video>` player, sourcing the video from `/api/video/{video_id}`.

---

## 5. Identified Bugs and Refactoring Opportunities

### High-Priority Issues

1.  **Brittle Code Parsing:**
    *   **Issue:** The entire script generation pipeline is initiated by parsing the Manim Python code with **regular expressions** (`text_extraction.py`). This is extremely fragile. Any small, valid deviation in the code style generated by Gemini could cause the parsing to fail, breaking the narration generation.
    *   **Recommendation:** The system should be refactored to use Python's Abstract Syntax Tree (`ast`) module. While more complex to implement, parsing the code with `ast` would create a robust and reliable representation of the code's structure, making the extraction of animations, text, and timings much more accurate and resilient to stylistic changes. The `ast` module is already imported but is not used.

2.  **Inaccurate Timing Heuristics:**
    *   **Issue:** When narration is extracted from high-level comments (`# narration:` or `# section:`), the timing is determined by distributing the total scene duration evenly among the comments. This is a rough heuristic that does not reflect the actual timing of animations on screen, likely leading to poor A/V sync.
    *   **Recommendation:** The prompt engineering in `gemini.py` should be updated to favor a more precise narration style. It should instruct the LLM to place narration comments *directly before* the `self.play()` calls they correspond to. The text extraction logic already supports this more accurate timing method, but the system doesn't guarantee its use.

### Medium-Priority Issues

3.  **Duplicated Code:**
    *   **Issue:** There are several instances of duplicated logic across different services.
        *   Narration script generation logic exists in both `manim.py` and `generate.py`.
        *   SSML enhancement logic is scattered between `sync.py` and `tts.py`, creating a circular dependency.
        *   A `generate_timing_map` method is defined in both `text_extraction.py` and `sync.py`.
    *   **Recommendation:** Consolidate shared logic into utility functions in `app/utils/helpers.py` or centralize responsibilities within a single service (e.g., all script creation and enhancement should live in `sync.py`).

4.  **Confusing and Redundant Flows:**
    *   **Issue:** There are two distinct ways to add narration to a video: the automatic flow that runs right after generation, and a manual flow triggered by the `/api/video/{video_id}/sync_narration` endpoint. It's unclear how these two flows interact, and it could lead to a race condition where both try to write the final narrated video at the same time.
    *   **Recommendation:** The flow should be simplified. The `sync_narration` endpoint should likely be used for *re-generating* narration with different parameters (e.g., a new voice), not as a primary generation method. The logic should be clarified to prevent conflicts.

5.  **Unused/Legacy Code:**
    *   **Issue:** The `media_processing.py` service contains multiple functions for merging audio (`merge_audio_segments_with_video`, `merge_audio_video_advanced`) that appear to be unused in the primary workflow, which uses the superior `merge_audio_segments_with_video_direct` method.
    *   **Recommendation:** Remove the dead code to simplify the service and improve maintainability. 