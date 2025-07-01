# EduTutor 

This is the frontend application for EduTutor, an AI-powered educational video generation platform.

## Setup

1. Install dependencies:
   ```
   npm install
   ```

2. Set up environment variables:
   Create a `.env.local` file in the frontend directory with the following variables:
   ```
   # Backend API URL
   BACKEND_API_URL=http://localhost:8000
   
   # Make this accessible to the browser
   NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
   ```

3. Run the development server:
   ```
   npm run dev
   ```

## Key Features

- Interactive educational video generation
- Real-time video status updates
- Video playback with custom controls
- Video download functionality

## Directory Structure

- `app/`: Next.js app directory
  - `page.tsx`: Home page with topic input
  - `video/`: Video player page
  - `api/`: API routes
    - `generate_manim/`: API route for generating Manim code
    - `fetch_video/`: API route for fetching video status
    - `video_stream/`: API route for streaming videos
- `components/`: Reusable UI components
- `lib/`: Utility functions and helpers
- `public/`: Static assets

## Video Generation Flow

1. User enters an educational topic on the home page
2. Frontend sends the topic to the backend via API
3. Backend generates Manim code and creates a video
4. Frontend polls for video status until complete
5. Video is displayed in the player when ready 