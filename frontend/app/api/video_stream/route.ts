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

    // Forward the request to the backend API
    const response = await fetch(`${BACKEND_API_URL}/api/video/file/${videoId}`);

    if (!response.ok) {
      return new Response(null, {
        status: response.status,
        statusText: response.statusText,
      });
    }

    // Get the video data as an array buffer
    const videoData = await response.arrayBuffer();
    
    // Create a new response with the video data and appropriate headers
    return new Response(videoData, {
      status: 200,
      headers: {
        'Content-Type': 'video/mp4',
        'Content-Disposition': `inline; filename="educational_video_${videoId}.mp4"`,
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