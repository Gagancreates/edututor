# Phase 1: Local Development with Manim Integration

## Overview
In Phase 1, we will implement the core functionality of EduTutor using local storage and computation. The goal is to create a working prototype where users can enter a prompt about what they want to learn or a math problem, and receive a generated educational video created with Manim.

## Step-by-Step Implementation Plan

### 1. Environment Setup (Backend)
1. **Set up FastAPI backend**
   - Create a new directory `backend` in the project root
   - Initialize a Python virtual environment
   ```bash
   mkdir backend
   cd backend
   python -m venv venv
   # Activate virtual environment (Windows)
   .\venv\Scripts\activate
   # Activate virtual environment (Linux/Mac)
   source venv/bin/activate
   ```
   
2. **Install required dependencies**
   ```bash
   pip install fastapi uvicorn python-dotenv manim google-generativeai pydantic
   ```
   
3. **Create basic FastAPI application structure**
   ```
   backend/
   ├── app/
   │   ├── __init__.py
   │   ├── main.py          # FastAPI entry point
   │   ├── routers/         # API route handlers
   │   │   ├── __init__.py
   │   │   └── generate.py  # Video generation endpoints
   │   ├── services/        # Business logic
   │   │   ├── __init__.py
   │   │   ├── gemini.py    # Gemini API integration
   │   │   └── manim.py     # Manim code generation and execution
   │   └── utils/           # Utility functions
   │       ├── __init__.py
   │       └── helpers.py
   ├── .env                 # Environment variables
   └── requirements.txt     # Python dependencies
   ```

### 2. Gemini API Integration
1. **Set up Gemini API client**
   - Create a `.env` file with Gemini API key
   - Implement a service to communicate with Gemini API

2. **Design the prompt engineering**
   - Create a masterful prompt that instructs Gemini to generate Manim code for educational content
   - The prompt should specify:
     - Clear instructions for creating Manim code that explains the concept
     - Guidelines for code structure and complexity
     - Requirements for educational value and visual clarity

3. **Implement prompt handling and response parsing**
   - Create functions to send user prompts to Gemini API
   - Parse and validate the returned Manim code

### 3. Manim Integration
1. **Set up Manim environment**
   - Ensure all Manim dependencies are installed (Cairo, FFmpeg, etc.)
   - Create a service to handle Manim code execution

2. **Implement code execution pipeline**
   - Create a temporary directory for each generation
   - Write the Gemini-generated Manim code to a Python file
   - Execute the Manim code and capture the output video
   - Handle errors and timeouts

3. **Video processing**
   - Implement functions to handle the generated video files
   - Set up temporary storage for videos
   - Create endpoints to serve the videos to the frontend

### 4. FastAPI Endpoints
1. **Create generation endpoint**
   ```python
   @router.post("/generate")
   async def generate_video(request: GenerateRequest):
       # 1. Get user prompt
       # 2. Send to Gemini API
       # 3. Parse response and extract Manim code
       # 4. Execute Manim code
       # 5. Return video file path or URL
   ```

2. **Create video serving endpoint**
   ```python
   @router.get("/video/{video_id}")
   async def get_video(video_id: str):
       # Serve the generated video file
   ```

3. **Implement error handling and validation**
   - Validate user input
   - Handle API errors
   - Implement proper error responses

### 5. Frontend-Backend Integration
1. **Update Next.js API routes to proxy to FastAPI**
   - Modify app/api/generate/route.ts to forward requests to the FastAPI backend
   ```typescript
   // app/api/generate/route.ts
   import { NextRequest, NextResponse } from 'next/server';
   
   export async function POST(req: NextRequest) {
     try {
       const body = await req.json();
       
       // Forward request to FastAPI backend
       const response = await fetch('http://localhost:8000/api/generate', {
         method: 'POST',
         headers: { 'Content-Type': 'application/json' },
         body: JSON.stringify(body)
       });
       
       const data = await response.json();
       return NextResponse.json(data);
     } catch (error) {
       return NextResponse.json({ error: 'Failed to generate video' }, { status: 500 });
     }
   }
   ```

2. **Create video status polling endpoint**
   - Add app/api/video/[videoId]/route.ts to check video generation status
   ```typescript
   // app/api/video/[videoId]/route.ts
   import { NextRequest, NextResponse } from 'next/server';
   
   export async function GET(req: NextRequest, { params }: { params: { videoId: string } }) {
     try {
       const videoId = params.videoId;
       
       // Check video status from backend
       const response = await fetch(`http://localhost:8000/api/video/${videoId}`);
       const data = await response.json();
       
       return NextResponse.json(data);
     } catch (error) {
       return NextResponse.json({ error: 'Failed to get video status' }, { status: 500 });
     }
   }
   ```

3. **Implement video streaming endpoint**
   - Create app/api/video/file/[videoId]/route.ts for video streaming
   ```typescript
   // app/api/video/file/[videoId]/route.ts
   import { NextRequest } from 'next/server';
   
   export async function GET(req: NextRequest, { params }: { params: { videoId: string } }) {
     try {
       const videoId = params.videoId;
       
       // Stream video from backend
       const response = await fetch(`http://localhost:8000/api/video/file/${videoId}`);
       
       // Return video stream
       return new Response(response.body, {
         headers: {
           'Content-Type': 'video/mp4',
           'Content-Disposition': `inline; filename="${videoId}.mp4"`
         }
       });
     } catch (error) {
       return new Response('Failed to stream video', { status: 500 });
     }
   }
   ```

4. **Update video generation component**
   - Modify components/video-generator.tsx to use the new API endpoints
   - Implement form validation for user prompts
   - Add complexity and duration options
   ```typescript
   // Example update to video-generator.tsx
   const handleSubmit = async (e: React.FormEvent) => {
     e.preventDefault();
     setIsLoading(true);
     
     try {
       const response = await fetch('/api/generate', {
         method: 'POST',
         headers: { 'Content-Type': 'application/json' },
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
       setError('Failed to generate video');
     } finally {
       setIsLoading(false);
     }
   };
   ```

5. **Implement status polling mechanism**
   - Create a polling function in video-generator.tsx to check video status
   - Update UI based on status changes
   - Handle different status states (processing, completed, failed)
   ```typescript
   const startPolling = (videoId: string) => {
     const interval = setInterval(async () => {
       try {
         const response = await fetch(`/api/video/${videoId}`);
         const data = await response.json();
         
         setStatus(data.status);
         
         if (data.status === 'completed') {
           setVideoUrl(data.url);
           clearInterval(interval);
         } else if (data.status === 'failed') {
           setError(data.message);
           clearInterval(interval);
         }
       } catch (error) {
         setError('Failed to check video status');
         clearInterval(interval);
       }
     }, 2000); // Poll every 2 seconds
     
     return () => clearInterval(interval);
   };
   ```

6. **Update video player component**
   - Enhance app/video/page.tsx to handle Manim videos
   - Implement video controls with play, pause, and seek functionality
   - Add error handling for video loading issues
   ```typescript
   // Example update to video player component
   import { useEffect, useRef } from 'react';
   
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

### 6. Local Storage Implementation
1. **Set up temporary file storage**
   - Create a directory structure for storing generated videos
   - Implement cleanup mechanisms to remove old files

2. **Implement basic caching**
   - Store generated videos with their corresponding prompts
   - Check cache before generating new videos for similar prompts

### 7. Testing and Debugging
1. **Create test cases**
   - Test the Gemini API integration
   - Test Manim code generation and execution
   - Test the end-to-end flow

2. **Implement logging**
   - Set up comprehensive logging for debugging
   - Log API requests, Manim execution, and errors

3. **Manual testing**
   - Test with various educational topics and math problems
   - Verify video quality and educational value

## Technical Considerations
1. **Manim Execution Environment**
   - Ensure Manim can run in a headless environment
   - Configure proper rendering settings for web delivery

2. **Performance Optimization**
   - Implement timeouts for Gemini API calls and Manim execution
   - Optimize video encoding for web streaming

3. **Security**
   - Validate and sanitize user input
   - Implement rate limiting
   - Ensure safe execution of generated code

## Completion Criteria
Phase 1 is complete when:
1. Users can enter educational topics or math problems
2. The system generates appropriate Manim code via Gemini API
3. The Manim code is executed successfully to create a video
4. The video is served back to the user through the frontend
5. The entire process works reliably on a local development environment 