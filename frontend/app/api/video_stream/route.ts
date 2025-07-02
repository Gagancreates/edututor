import { NextRequest, NextResponse } from 'next/server';

// Backend API URL
const BACKEND_API_URL = process.env.BACKEND_API_URL || 'http://localhost:8000';

export async function GET(request: NextRequest) {
  try {
    // Get videoId from the URL
    const { searchParams } = new URL(request.url);
    const videoId = searchParams.get('videoId');
    
    if (!videoId) {
      return NextResponse.json(
        { error: 'Video ID is required' },
        { status: 400 }
      );
    }

    console.log(`Streaming video for ID: ${videoId}`);

    // Forward the request to the backend API
    const response = await fetch(`${BACKEND_API_URL}/api/video/${videoId}`, {
      method: 'GET',
      // Add a longer timeout for video streaming
      signal: AbortSignal.timeout(30000), // 30 seconds timeout
    });

    if (!response.ok) {
      console.error(`Error streaming video: ${response.status} ${response.statusText}`);
      
      // Try to get error details if available
      let errorDetail = response.statusText;
      try {
        const errorData = await response.json();
        if (errorData.detail) {
          errorDetail = errorData.detail;
        }
      } catch (e) {
        // Ignore JSON parsing errors
      }
      
      return NextResponse.json(
        { error: `Failed to stream video: ${errorDetail}` },
        { status: response.status }
      );
    }

    // Get the video data as an array buffer
    const videoData = await response.arrayBuffer();
    
    if (!videoData || videoData.byteLength === 0) {
      console.error('Received empty video data from backend');
      return NextResponse.json(
        { error: 'Received empty video data from backend' },
        { status: 500 }
      );
    }
    
    console.log(`Successfully received video data: ${videoData.byteLength} bytes`);
    
    // Create a new response with the video data and appropriate headers
    return new Response(videoData, {
      status: 200,
      headers: {
        'Content-Type': 'video/mp4',
        'Content-Disposition': `inline; filename="educational_video_${videoId}.mp4"`,
        'Cache-Control': 'public, max-age=3600', // Cache for 1 hour
      },
    });
    
  } catch (error) {
    console.error('Error streaming video:', error);
    return NextResponse.json(
      { error: 'Failed to stream video' },
      { status: 500 }
    );
  }
} 