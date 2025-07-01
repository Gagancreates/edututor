# Detailed Technical Flow: User Prompt to Video Rendering

## 1. User Input (Frontend)
- User enters prompt in `components/video-generator.tsx`
- Form captures prompt text, complexity level, and duration settings
- Form submission triggers `handleSubmit()` function

## 2. Frontend API Request
- `components/video-generator.tsx` sends POST request to `/api/generate` 
- Request body contains: `{ prompt, complexity, duration }`
- Sets loading state to show progress indicator

## 3. Next.js API Route
- `app/api/generate/route.ts` receives the request
- Extracts request body using `req.json()`
- Forwards request to FastAPI backend via fetch:
  ```typescript
  fetch('http://localhost:8000/api/generate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body)
  })
  ```

## 4. FastAPI Backend Processing
- `backend/app/routers/generate.py` receives request at `@router.post("/generate")` endpoint
- Validates request using Pydantic model `GenerateRequest`
- Generates unique video ID using `generate_unique_id()` from `utils/helpers.py`

## 5. Gemini API Integration
- `backend/app/services/gemini.py` processes the prompt
- `generate_manim_code()` function crafts a system prompt with instructions
- Sends request to Gemini API using `model.generate_content_async()`
- Receives and validates Manim code in the response

## 6. Background Video Generation
- FastAPI endpoint adds Manim execution to background tasks:
  ```python
  background_tasks.add_task(execute_manim_code, video_id=video_id, manim_code=manim_code)
  ```
- Returns immediate response with `video_id` and `status: "processing"`

## 7. Manim Code Execution
- `backend/app/services/manim.py` handles video generation
- `execute_manim_code()` creates temporary directory
- Writes Manim code to Python file
- Executes Manim with subprocess using asyncio:
  ```python
  process = await asyncio.create_subprocess_exec(
      "manim", "-qm", "--output_file", f"{video_id}", 
      "--media_dir", str(output_dir), str(script_path), "CreateScene"
  )
  ```

## 8. FFmpeg Processing
- Manim internally uses FFmpeg to render the animation frames into a video
- FFmpeg combines the rendered frames into an MP4 file
- Output video is saved to `videos/{video_id}/` directory

## 9. Frontend Polling
- `components/video-generator.tsx` starts polling with `startPolling(video_id)`
- Sends GET requests to `/api/video/{video_id}` every 2 seconds
- Next.js route `app/api/video/[videoId]/route.ts` forwards requests to FastAPI

## 10. Status Checking
- FastAPI endpoint `@router.get("/video/{video_id}")` receives status check
- `backend/app/utils/helpers.py` checks video status with `get_video_status()`
- Returns status: "processing", "completed", or "failed"
- When complete, includes video URL in response

## 11. Video Streaming
- When status is "completed", frontend receives URL to video
- Frontend makes request to `/api/video/file/{video_id}`
- Next.js route `app/api/video/file/[videoId]/route.ts` forwards to FastAPI
- FastAPI endpoint `@router.get("/video/file/{video_id}")` serves video:
  ```python
  return FileResponse(path=video_path, media_type="video/mp4", filename=f"{video_id}.mp4")
  ```

## 12. Video Display
- `app/video/page.tsx` receives video URL
- Renders video using HTML5 video element with controls
- User can play, pause, and control the educational video

## 13. Error Handling
- Error handling at each step with appropriate status codes
- Frontend displays error messages if any step fails
- Backend logs errors and creates error files for debugging

This end-to-end flow creates a seamless experience where the user submits a prompt and receives an educational video generated with Manim, with FFmpeg handling the final video encoding.