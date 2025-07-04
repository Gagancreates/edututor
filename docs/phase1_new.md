# Phase 1: Local Development with Manim Integration

## Overview
In Phase 1, we will implement the core functionality of EduTutor using local storage and computation. The goal is to create a working prototype where users can enter a prompt about what they want to learn or a math problem, and receive a generated educational video created with Manim.

## Step-by-Step Implementation Checklist

### 1. Environment Setup (Backend)
1.  **Create FastAPI project structure**
   - Create directory structure with routers, services, and utils folders
   - Set up __init__.py files in each directory
   - Create main.py as the FastAPI entry point

2.  **Set up Python environment**
   - Create and activate virtual environment
   ```bash
   mkdir backend
   cd backend
   python -m venv venv
   # Activate virtual environment (Windows)
   .\venv\Scripts\activate
   # Activate virtual environment (Linux/Mac)
   source venv/bin/activate
   ```

3.  **Install required dependencies**
   ```bash
   pip install fastapi uvicorn python-dotenv manim google-generativeai pydantic python-multipart aiofiles
   ```

4.  **Install system dependencies**
   - Install FFmpeg for video processing
   - Install Cairo for Manim rendering
   - Verify all dependencies are working with a simple test

### 2. Gemini API Integration
1.  **Configure API credentials**
   - Create .env file in backend directory
   - Add Gemini API key to .env file
   ```
   GEMINI_API_KEY=your-gemini-api-key-here
   ```
   - Implement environment loading in gemini.py

2.  **Create Gemini service**
   - Implement the gemini.py service with API client setup
   - Create generate_manim_code() function with proper error handling
   - Test the API connection with a simple prompt

3.  **Design prompt engineering system**
   - Create a detailed system prompt for Gemini in gemini.py
   - Include specific instructions for Manim code generation
   - Test different prompt variations to optimize output quality

### 3. Manim Integration
1.  **Create Manim execution service**
   - Implement manim.py with execute_manim_code() function
   - Set up proper subprocess handling with asyncio
   - Configure timeout and error handling

2.  **Set up video storage system**
   - Create videos directory structure
   - Implement unique ID generation for video files
   - Configure proper file paths and permissions

3.  **Implement video processing pipeline**
   - Create function to write Manim code to temporary files
   - Set up Manim command execution with proper flags
   - Implement video file handling and cleanup

### 4. FastAPI Endpoints Development
1.  **Create API router structure**
   - Set up generate.py with router definition
   - Define request and response models using Pydantic

2.  **Implement generation endpoint**
   - Create POST /api/generate endpoint
   - Implement request validation and error handling
   - Connect endpoint to Gemini and Manim services
   ```python
   @router.post("/generate", response_model=GenerateResponse)
   async def generate_video(request: GenerateRequest, background_tasks: BackgroundTasks):
       # Generate unique ID
       video_id = generate_unique_id()
       
       # Get Manim code from Gemini
       manim_code = await generate_manim_code(request.prompt, request.complexity, request.duration)
       
       # Execute Manim in background
       background_tasks.add_task(execute_manim_code, video_id=video_id, manim_code=manim_code)
       
       return {"video_id": video_id, "status": "processing"}
   ```

3.  **Implement video serving endpoints**
   - Create GET /api/video/{video_id} endpoint for status checking
   - Create GET /api/video/file/{video_id} endpoint for video streaming
   ```python
   @router.get("/video/file/{video_id}")
   async def get_video_file(video_id: str):
       video_path = get_video_path(video_id)
       if not video_path:
           raise HTTPException(status_code=404, detail="Video not found")
       
       return FileResponse(path=video_path, media_type="video/mp4", filename=f"{video_id}.mp4")
   ```

4.  **Add CORS and middleware configuration**
   - Configure CORS in main.py to allow frontend requests
   - Add appropriate middleware for error handling
   - Test API endpoints with tools like curl or Postman

### 5. Frontend-Backend Integration
1.  **Update Next.js API routes**
   - Modify app/api/generate/route.ts to proxy requests to FastAPI
   ```typescript
   // app/api/generate/route.ts
   import { NextRequest, NextResponse } from "next/server";
   
   export async function POST(req: NextRequest) {
     try {
       const body = await req.json();
       
       // Forward request to FastAPI backend
       const response = await fetch("http://localhost:8000/api/generate", {
         method: "POST",
         headers: { "Content-Type": "application/json" },
         body: JSON.stringify(body)
       });
       
       const data = await response.json();
       return NextResponse.json(data);
     } catch (error) {
       return NextResponse.json({ error: "Failed to generate video" }, { status: 500 });
     }
   }
   ```

2.  **Create video status polling system**
   - Add app/api/video/[videoId]/route.ts to check video status
   ```typescript
   // app/api/video/[videoId]/route.ts
   import { NextRequest, NextResponse } from "next/server";
   
   export async function GET(req: NextRequest, { params }: { params: { videoId: string } }) {
     try {
       const videoId = params.videoId;
       
       // Check video status from backend
       const response = await fetch(`http://localhost:8000/api/video/${videoId}`);
       const data = await response.json();
       
       return NextResponse.json(data);
     } catch (error) {
       return NextResponse.json({ error: "Failed to get video status" }, { status: 500 });
     }
   }
   ```

3.  **Implement video streaming endpoint**
   - Create app/api/video/file/[videoId]/route.ts for video streaming
   ```typescript
   // app/api/video/file/[videoId]/route.ts
   import { NextRequest } from "next/server";
   
   export async function GET(req: NextRequest, { params }: { params: { videoId: string } }) {
     try {
       const videoId = params.videoId;
       
       // Stream video from backend
       const response = await fetch(`http://localhost:8000/api/video/file/${videoId}`);
       
       // Return video stream
       return new Response(response.body, {
         headers: {
           "Content-Type": "video/mp4",
           "Content-Disposition": `inline; filename="${videoId}.mp4"`
         }
       });
     } catch (error) {
       return new Response("Failed to stream video", { status: 500 });
     }
   }
   ```

### 6. Frontend Components Update
1.  **Update video generator component**
   - Modify components/video-generator.tsx to use the new API
   - Implement form validation for user prompts
   - Add complexity and duration options
   ```typescript
   // Example update to video-generator.tsx
   const handleSubmit = async (e: React.FormEvent) => {
     e.preventDefault();
     setIsLoading(true);
     
     try {
       const response = await fetch("/api/generate", {
         method: "POST",
         headers: { "Content-Type": "application/json" },
         body: JSON.stringify({ 
           prompt: prompt,
           complexity: complexity,
           duration: duration
         })
       });
       
       const data = await response.json();
       setVideoId(data.video_id);
       startPolling(data.video_id);
     } catch (error) {
       setError("Failed to generate video");
     } finally {
       setIsLoading(false);
     }
   };
   ```

2.  **Implement status polling mechanism**
   - Create a polling function to check video generation status
   - Update UI based on status changes
   - Handle different status states (processing, completed, failed)
   ```typescript
   const startPolling = (videoId: string) => {
     const interval = setInterval(async () => {
       try {
         const response = await fetch(`/api/video/${videoId}`);
         const data = await response.json();
         
         setStatus(data.status);
         
         if (data.status === "completed") {
           setVideoUrl(data.url);
           clearInterval(interval);
         } else if (data.status === "failed") {
           setError(data.message);
           clearInterval(interval);
         }
       } catch (error) {
         setError("Failed to check video status");
         clearInterval(interval);
       }
     }, 2000); // Poll every 2 seconds
     
     return () => clearInterval(interval);
   };
   ```

3.  **Update video player component**
   - Enhance app/video/page.tsx to handle Manim videos
   - Implement video controls with play, pause, and seek functionality
   - Add error handling for video loading issues
   ```typescript
   // Example update to video player component
   import { useEffect, useRef } from "react";
   
   export default function VideoPlayer({ videoUrl }) {
     const videoRef = useRef<HTMLVideoElement>(null);
     
     useEffect(() => {
       if (videoRef.current && videoUrl) {
         videoRef.current.load();
       }
     }, [videoUrl]);
     
     return (
       <div className="video-container">
         <video 
           ref={videoRef}
           controls
           className="w-full rounded-lg shadow-lg"
         >
           <source src={videoUrl} type="video/mp4" />
           Your browser does not support the video tag.
         </video>
       </div>
     );
   }
   ```

### 7. Video Storage and Caching
1.  **Implement temporary storage system**
   - Create directory structure for video storage
   ```bash
   mkdir -p backend/videos
   ```
   - Implement file management in helpers.py
   - Add file cleanup for old videos

2.  **Add video metadata storage**
   - Create simple JSON-based storage for video metadata
   - Store prompt, generation time, and video path
   - Implement functions to read and write metadata

3.  **Implement basic caching mechanism**
   - Add functions to check for existing videos with similar prompts
   - Implement cache hit/miss logic in generate endpoint
   - Add cache invalidation for old entries

### 8. Testing and Debugging
1.  **Set up comprehensive logging**
   - Configure logging in main.py
   ```python
   import logging
   
   logging.basicConfig(
       level=logging.INFO,
       format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
       handlers=[
           logging.FileHandler("app.log"),
           logging.StreamHandler()
       ]
   )
   ```
   - Add log statements throughout the application
   - Create debug endpoints for troubleshooting

2.  **Test Gemini API integration**
   - Create test script for Gemini API
   - Verify prompt engineering effectiveness
   - Test error handling and response parsing

3.  **Test Manim code execution**
   - Create test script for Manim execution
   - Verify video generation with sample code
   - Test error handling for invalid Manim code

4.  **Test end-to-end flow**
   - Test the complete flow from user prompt to video display
   - Verify all components work together correctly
   - Document any issues and fix them

### 9. Performance and Security
1.  **Implement timeouts and rate limiting**
   - Add timeouts for Gemini API calls
   - Add timeouts for Manim execution
   - Implement basic rate limiting for API endpoints

2.  **Optimize video encoding**
   - Configure FFmpeg parameters for web streaming
   - Balance quality and file size
   - Test video playback performance

3.  **Implement input validation and sanitization**
   - Add comprehensive validation for user inputs
   - Sanitize inputs before processing
   - Implement safe code execution practices

## Completion Criteria
Phase 1 is complete when:
1. Users can enter educational topics or math problems through the frontend
2. The system successfully generates Manim code via Gemini API
3. Manim code is executed with FFmpeg to create a video
4. The video is properly streamed back to the frontend
5. Users can view and control the educational video playback
6. The entire process works reliably on a local development environment
