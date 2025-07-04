"use client"

import { useState, useEffect, useRef, Suspense } from "react"
import { Button } from "@/components/ui/button"
import { ArrowLeft, Download, Play, Pause, Volume2, VolumeX, Share2, RotateCcw, Heart, Loader2, Maximize, Minimize } from "lucide-react"
import { motion } from "framer-motion"
import Link from "next/link"
import { useSearchParams } from "next/navigation"

function VideoPlayerContent() {
  const searchParams = useSearchParams()
  const topic = searchParams.get("topic") || "Educational Topic"
  const videoId = searchParams.get("videoId")

  const [isPlaying, setIsPlaying] = useState(false)
  const [isMuted, setIsMuted] = useState(false)
  const [progress, setProgress] = useState(0)
  const [duration, setDuration] = useState(0)
  const [currentSubtitle, setCurrentSubtitle] = useState("")
  const [isFullscreen, setIsFullscreen] = useState(false)
  const [showTimeTooltip, setShowTimeTooltip] = useState(false)
  const [tooltipTime, setTooltipTime] = useState(0)
  const [tooltipPosition, setTooltipPosition] = useState(0)
  const [isDragging, setIsDragging] = useState(false)
  const [videoStatus, setVideoStatus] = useState({
    status: "loading", // loading, processing, completed, failed
    message: "Checking video status...",
    video_url: null  // Match the backend response structure
  })
  
  const videoRef = useRef<HTMLVideoElement>(null)
  const videoContainerRef = useRef<HTMLDivElement>(null)
  const progressBarRef = useRef<HTMLDivElement>(null)

  const subtitles = [
    "Welcome to this educational video about " + topic,
    "Let's explore the fundamental concepts together",
    "This visualization will help you understand the key principles",
    "Notice how the elements interact with each other",
    "This demonstrates the core theory in action",
  ]

  // Fetch video status
  useEffect(() => {
    if (!videoId) return
    
    const fetchVideoStatus = async () => {
      try {
        const response = await fetch(`/api/fetch_video?videoId=${videoId}`)
        
        if (!response.ok) {
          throw new Error('Failed to fetch video status')
        }
        
        const data = await response.json()
        setVideoStatus(data)
        
        // If video is still processing, poll again in a few seconds
        if (data.status === 'processing') {
          setTimeout(fetchVideoStatus, 3000)
        }
      } catch (error) {
        console.error('Error fetching video status:', error)
        setVideoStatus({
          status: 'failed',
          message: 'Failed to fetch video status',
          video_url: null
        })
      }
    }
    
    fetchVideoStatus()
  }, [videoId])

  // Handle video playback
  useEffect(() => {
    if (!videoRef.current) return
    
    if (isPlaying) {
      videoRef.current.play().catch(error => {
        console.error('Error playing video:', error)
        setIsPlaying(false)
      })
    } else {
      videoRef.current.pause()
    }
  }, [isPlaying])

  // Handle video loading error or status response
  const handleVideoError = async (e: React.SyntheticEvent<HTMLVideoElement, Event>) => {
    console.error("Error loading video:", e);
    
    // Try to check if this is a status response
    try {
      const videoSrc = `/api/video_stream?videoId=${videoId}&t=${new Date().getTime()}`;
      const response = await fetch(videoSrc);
      
      // Check if we got a JSON response (status update) instead of video
      const contentType = response.headers.get('content-type');
      if (contentType && contentType.includes('application/json')) {
        const statusData = await response.json();
        
        // If this is a status response, update our status
        if (statusData.isStatusResponse) {
          console.log("Received status response instead of video:", statusData);
          setVideoStatus({
            status: statusData.status,
            message: statusData.message,
            video_url: statusData.video_url || null
          });
          
          // If still processing, poll again in a few seconds
          if (statusData.status === 'processing') {
            setTimeout(() => {
              // Force video element to reload
              if (videoRef.current) {
                const currentSrc = videoRef.current.src;
                videoRef.current.src = '';
                setTimeout(() => {
                  if (videoRef.current) {
                    videoRef.current.src = currentSrc;
                    videoRef.current.load();
                  }
                }, 100);
              }
            }, 3000);
          }
          
          return;
        }
      }
      
      // If we got here, it's a real error
      setVideoStatus({
        status: 'failed',
        message: "Failed to load video. The video file may be corrupted or inaccessible.",
        video_url: null
      });
    } catch (error) {
      console.error("Error handling video error:", error);
      setVideoStatus({
        status: 'failed',
        message: "Failed to load video. The video file may be corrupted or inaccessible.",
        video_url: null
      });
    }
  };

  // Update progress for placeholder animation or real video
  useEffect(() => {
    if (videoStatus.status === 'completed' && videoRef.current) {
      // For real video, use timeupdate event
      const updateProgress = () => {
        if (!videoRef.current) return
        const currentProgress = (videoRef.current.currentTime / videoRef.current.duration) * 100
        setProgress(currentProgress)
      }
      
      videoRef.current.addEventListener('timeupdate', updateProgress)
      videoRef.current.addEventListener('loadedmetadata', () => {
        if (videoRef.current) {
          setDuration(videoRef.current.duration)
          console.log("Video duration loaded:", videoRef.current.duration)
        }
      })
      
      // Set duration if already loaded
      if (videoRef.current.duration) {
        setDuration(videoRef.current.duration)
      }
      
      return () => {
        if (videoRef.current) {
          videoRef.current.removeEventListener('timeupdate', updateProgress)
        }
      }
    } else if (videoStatus.status === 'processing' && isPlaying) {
      // For placeholder animation, use interval
      const interval = setInterval(() => {
        setProgress((prev) => {
          if (prev >= 100) {
            setIsPlaying(false)
            return 100
          }
          return prev + 0.5
        })
      }, 100)

      const subtitleInterval = setInterval(() => {
        const subtitleIndex = Math.floor((progress / 100) * subtitles.length)
        setCurrentSubtitle(subtitles[subtitleIndex] || "")
      }, 2000)

      return () => {
        clearInterval(interval)
        clearInterval(subtitleInterval)
      }
    }
  }, [isPlaying, subtitles, videoStatus.status]) // Removed progress from dependencies to avoid circular updates

  const togglePlay = () => setIsPlaying(!isPlaying)
  
  const toggleMute = () => {
    setIsMuted(!isMuted)
    if (videoRef.current) {
      videoRef.current.muted = !isMuted
    }
  }
  
  const resetVideo = () => {
    setProgress(0)
    if (videoRef.current) {
      videoRef.current.currentTime = 0
    }
    setIsPlaying(true)
  }
  
  // Format time in MM:SS format
  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60)
    const secs = Math.floor(seconds % 60)
    return `${mins}:${secs < 10 ? '0' : ''}${secs}`
  }
  
  // Handle video download
  const handleDownload = () => {
    if (videoStatus.status === 'completed' && videoId) {
      window.open(`/api/video_stream?videoId=${videoId}`, '_blank')
    }
  }

  // Handle fullscreen toggle
  const toggleFullscreen = () => {
    if (!videoContainerRef.current) return
    
    if (!isFullscreen) {
      if (videoContainerRef.current.requestFullscreen) {
        videoContainerRef.current.requestFullscreen()
      } else if ((videoContainerRef.current as any).webkitRequestFullscreen) {
        (videoContainerRef.current as any).webkitRequestFullscreen()
      } else if ((videoContainerRef.current as any).msRequestFullscreen) {
        (videoContainerRef.current as any).msRequestFullscreen()
      }
      setIsFullscreen(true)
    } else {
      if (document.exitFullscreen) {
        document.exitFullscreen()
      } else if ((document as any).webkitExitFullscreen) {
        (document as any).webkitExitFullscreen()
      } else if ((document as any).msExitFullscreen) {
        (document as any).msExitFullscreen()
      }
      setIsFullscreen(false)
    }
  }

  // Listen for fullscreen changes
  useEffect(() => {
    const handleFullscreenChange = () => {
      setIsFullscreen(!!document.fullscreenElement)
    }
    
    document.addEventListener('fullscreenchange', handleFullscreenChange)
    document.addEventListener('webkitfullscreenchange', handleFullscreenChange)
    document.addEventListener('mozfullscreenchange', handleFullscreenChange)
    document.addEventListener('MSFullscreenChange', handleFullscreenChange)
    
    return () => {
      document.removeEventListener('fullscreenchange', handleFullscreenChange)
      document.removeEventListener('webkitfullscreenchange', handleFullscreenChange)
      document.removeEventListener('mozfullscreenchange', handleFullscreenChange)
      document.removeEventListener('MSFullscreenChange', handleFullscreenChange)
    }
  }, [])
  
  // Handle progress bar hover and seeking
  const handleProgressHover = (e: React.MouseEvent<HTMLDivElement>) => {
    if (!progressBarRef.current || videoStatus.status !== 'completed' || !videoRef.current) return
    
    const rect = progressBarRef.current.getBoundingClientRect()
    const pos = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width))
    
    if (videoRef.current.duration && !isNaN(videoRef.current.duration)) {
      const time = pos * videoRef.current.duration
      setTooltipTime(time)
      setTooltipPosition(pos * 100)
      setShowTimeTooltip(true)
    }
  }
  
  const handleProgressLeave = () => {
    if (!isDragging) {
      setShowTimeTooltip(false)
    }
  }
  
  // Fixed seek function
  const seekVideo = (timePercent: number) => {
    if (!videoRef.current || videoStatus.status !== 'completed') return;
    
    // Wait for video to be fully loaded
    if (!videoRef.current.duration || isNaN(videoRef.current.duration)) {
      console.warn("Video duration not available yet");
      return;
    }
    
    try {
      const seekTime = Math.max(0, Math.min(videoRef.current.duration, (timePercent / 100) * videoRef.current.duration));
      console.log(`Seeking video to ${seekTime}s (${timePercent}%)`);
      
      // Pause the video before seeking to prevent issues
      const wasPlaying = !videoRef.current.paused;
      videoRef.current.pause();
      
      videoRef.current.currentTime = seekTime;
      
      // Resume playing if it was playing before
      if (wasPlaying) {
        videoRef.current.play().catch(console.error);
      }
    } catch (error) {
      console.error("Error seeking video:", error);
    }
  }
  
  // Fixed progress click handler
  const handleProgressClick = (e: React.MouseEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    
    if (!videoRef.current || !progressBarRef.current || videoStatus.status !== 'completed') return
    
    const rect = progressBarRef.current.getBoundingClientRect()
    const pos = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width))
    const timePercent = pos * 100;
    
    console.log(`Progress clicked at ${timePercent}%`);
    
    seekVideo(timePercent);
    
    if (videoRef.current.duration && !isNaN(videoRef.current.duration)) {
      setTooltipTime(pos * videoRef.current.duration)
      setTooltipPosition(timePercent)
    }
  }
  
  // Fixed mouse down handler for dragging
  const handleMouseDown = (e: React.MouseEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    
    if (videoStatus.status !== 'completed' || !videoRef.current || !progressBarRef.current) return
    
    setIsDragging(true)
    
    // Initial click position
    const rect = progressBarRef.current.getBoundingClientRect()
    const pos = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width))
    const timePercent = pos * 100;
    
    seekVideo(timePercent);
    
    const handleMouseMove = (e: MouseEvent) => {
      if (!videoRef.current || !progressBarRef.current) return
      
      const rect = progressBarRef.current.getBoundingClientRect()
      const pos = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width))
      const timePercent = pos * 100;
      
      // Update progress and seek during drag
      setProgress(timePercent);
      seekVideo(timePercent);
      
      if (videoRef.current.duration && !isNaN(videoRef.current.duration)) {
        setTooltipTime(pos * videoRef.current.duration)
        setTooltipPosition(timePercent)
      }
    }
    
    const handleMouseUp = () => {
      setIsDragging(false)
      setShowTimeTooltip(false)
      
      document.removeEventListener('mousemove', handleMouseMove)
      document.removeEventListener('mouseup', handleMouseUp)
    }
    
    document.addEventListener('mousemove', handleMouseMove)
    document.addEventListener('mouseup', handleMouseUp)
  }

  return (
    <div className="min-h-screen bg-black relative overflow-hidden">
      {/* Background effects */}
      <div className="absolute inset-0 bg-[linear-gradient(rgba(79,70,229,0.03)_1px,transparent_1px),linear-gradient(90deg,rgba(79,70,229,0.03)_1px,transparent_1px)] bg-[size:50px_50px] [mask-image:radial-gradient(ellipse_80%_50%_at_50%_0%,#000_70%,transparent_110%)]" />

      <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-blue-500/5 rounded-full blur-3xl" />
      <div className="absolute bottom-1/4 right-1/4 w-80 h-80 bg-purple-500/5 rounded-full blur-3xl" />

      <div className="relative z-10 container mx-auto px-6 py-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex items-center justify-between mb-8"
        >
          <Link href="/">
            <Button variant="ghost" className="text-gray-400 hover:text-white hover:bg-white/10 rounded-xl">
              <ArrowLeft className="mr-2 h-5 w-5" />
              Back to Home
            </Button>
          </Link>

          <div className="flex items-center gap-3">
            <Button variant="ghost" size="icon" className="text-gray-400 hover:text-white hover:bg-white/10 rounded-xl">
              <Heart className="h-5 w-5" />
            </Button>
            <Button variant="ghost" size="icon" className="text-gray-400 hover:text-white hover:bg-white/10 rounded-xl">
              <Share2 className="h-5 w-5" />
            </Button>
          </div>
        </motion.div>

        {/* Video Player */}
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          className="max-w-6xl mx-auto"
        >
          <div className="mb-6">
            <h1 className="font-bold text-3xl md:text-4xl text-white mb-2">{topic}</h1>
            <p className="text-gray-400">Generated educational video • AI-powered visualization</p>
          </div>

          {/* Main Video Container */}
          <div 
            ref={videoContainerRef}
            className={`relative bg-gradient-to-br from-gray-900 to-black rounded-3xl overflow-hidden border border-gray-800 shadow-2xl ${isFullscreen ? 'fullscreen-video' : ''}`}
          >
            {/* Video Canvas Area */}
            <div className="relative aspect-video bg-gradient-to-br from-blue-500/10 via-purple-500/10 to-cyan-500/10">
              {videoStatus.status === 'completed' && videoId ? (
                <video 
                  ref={videoRef}
                  className="w-full h-full object-contain"
                  controls={false}
                  muted={isMuted}
                  playsInline
                  onEnded={() => setIsPlaying(false)}
                  onLoadedData={() => {
                    console.log("Video loaded successfully")
                    if (videoRef.current) {
                      console.log("Video duration on load:", videoRef.current.duration)
                      setDuration(videoRef.current.duration)
                    }
                  }}
                  onError={handleVideoError}
                >
                  <source 
                    src={`/api/video_stream?videoId=${videoId}&t=${new Date().getTime()}`} 
                    type="video/mp4" 
                  />
                  Your browser does not support the video tag.
                </video>
              ) : (
                <>
                  {/* Loading or Processing State */}
                  {videoStatus.status === 'loading' || videoStatus.status === 'processing' ? (
                    <div className="absolute inset-0 flex flex-col items-center justify-center">
                      {videoStatus.status === 'loading' ? (
                        <>
                          <Loader2 className="h-12 w-12 text-blue-500 animate-spin mb-4" />
                          <p className="text-white text-xl">Checking video status...</p>
                        </>
                      ) : (
                        <>
                          {/* Simulated p5.js Animation for processing state */}
                          <motion.div
                            animate={{
                              scale: [1, 1.2, 1],
                              rotate: [0, 180, 360],
                            }}
                            transition={{
                              duration: 4,
                              repeat: Number.POSITIVE_INFINITY,
                              ease: "easeInOut",
                            }}
                            className="w-32 h-32 bg-gradient-to-br from-blue-400 to-purple-400 rounded-full opacity-60 mb-6"
                          />
                          <p className="text-white text-xl">Processing your video...</p>
                          <p className="text-gray-400 mt-2">{videoStatus.message}</p>
                        </>
                      )}
                    </div>
                  ) : videoStatus.status === 'failed' ? (
                    <div className="absolute inset-0 flex flex-col items-center justify-center">
                      <div className="text-red-500 text-5xl mb-4">✗</div>
                      <p className="text-white text-xl">Video generation failed</p>
                      <p className="text-gray-400 mt-2">{videoStatus.message}</p>
                      <Button 
                        onClick={() => window.location.href = '/'}
                        className="mt-6 bg-blue-600 hover:bg-blue-700"
                      >
                        Try Again
                      </Button>
                    </div>
                  ) : null}

                  {/* Subtitles for processing state */}
                  {videoStatus.status === 'processing' && (
                    <div className="absolute bottom-0 left-0 right-0 p-6">
                      <div className="bg-black/70 backdrop-blur-sm rounded-xl p-4 text-center">
                        <p className="text-white text-lg">{currentSubtitle}</p>
                      </div>
                    </div>
                  )}
                </>
              )}

              {/* Play/Pause Overlay */}
              {!isPlaying && videoStatus.status === 'completed' && (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="absolute inset-0 flex items-center justify-center bg-black/20 backdrop-blur-sm"
                >
                  <Button
                    onClick={togglePlay}
                    size="lg"
                    className="bg-white/20 hover:bg-white/30 text-white rounded-full w-20 h-20 backdrop-blur-sm border border-white/20"
                  >
                    <Play className="h-8 w-8 ml-1" />
                  </Button>
                </motion.div>
              )}
            </div>

            {/* Controls - Only show for completed or processing videos */}
            {(videoStatus.status === 'completed' || videoStatus.status === 'processing') && (
              <div className="p-6 bg-gradient-to-r from-gray-900/90 to-black/90 backdrop-blur-sm">
                {/* Progress Bar */}
                <div className="mb-4" onClick={(e) => e.stopPropagation()}>
                  <div className="flex items-center justify-between text-sm text-gray-400 mb-2">
                    <span>
                      {videoStatus.status === 'completed' && duration > 0
                        ? formatTime(duration * (progress / 100))
                        : Math.floor((progress / 100) * 120) + 's'}
                    </span>
                    <span>
                      {videoStatus.status === 'completed' && duration > 0
                        ? formatTime(duration)
                        : '120s'}
                    </span>
                  </div>
                  <div 
                    ref={progressBarRef}
                    className="w-full bg-gray-700 rounded-full h-6 cursor-pointer relative flex items-center"
                    onClick={handleProgressClick}
                    onMouseMove={handleProgressHover}
                    onMouseLeave={handleProgressLeave}
                    onMouseDown={handleMouseDown}
                    style={{ zIndex: 10 }}
                  >
                    <div
                      className="absolute left-0 top-1/2 transform -translate-y-1/2 bg-gradient-to-r from-blue-500 to-purple-500 h-2 rounded-full transition-all duration-150"
                      style={{ width: `${progress}%` }}
                    />
                    
                    {/* Time tooltip on hover */}
                    {showTimeTooltip && videoStatus.status === 'completed' && (
                      <div 
                        className="absolute bottom-8 bg-black/80 text-white px-2 py-1 rounded text-xs transform -translate-x-1/2 pointer-events-none whitespace-nowrap"
                        style={{ left: `${tooltipPosition}%` }}
                      >
                        {formatTime(tooltipTime)}
                      </div>
                    )}
                    
                    {/* Draggable progress handle */}
                    {videoStatus.status === 'completed' && (
                      <div 
                        className="absolute top-1/2 w-4 h-4 bg-white rounded-full shadow-md transform -translate-y-1/2 -translate-x-1/2 cursor-pointer transition-opacity duration-150"
                        style={{ 
                          left: `${progress}%`,
                          opacity: (showTimeTooltip || isDragging) ? 1 : 0
                        }}
                      />
                    )}
                  </div>
                </div>

                {/* Control Buttons */}
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <Button
                      onClick={togglePlay}
                      variant="ghost"
                      size="icon"
                      className="text-white hover:bg-white/10 rounded-full w-12 h-12"
                      disabled={videoStatus.status !== 'completed'}
                    >
                      {isPlaying ? <Pause className="h-6 w-6" /> : <Play className="h-6 w-6 ml-0.5" />}
                    </Button>

                    <Button
                      onClick={toggleMute}
                      variant="ghost"
                      size="icon"
                      className="text-white hover:bg-white/10 rounded-full w-12 h-12"
                      disabled={videoStatus.status !== 'completed'}
                    >
                      {isMuted ? <VolumeX className="h-5 w-5" /> : <Volume2 className="h-5 w-5" />}
                    </Button>

                    <Button
                      onClick={resetVideo}
                      variant="ghost"
                      size="icon"
                      className="text-white hover:bg-white/10 rounded-full w-12 h-12"
                      disabled={videoStatus.status !== 'completed'}
                    >
                      <RotateCcw className="h-5 w-5" />
                    </Button>
                    
                    <Button
                      onClick={toggleFullscreen}
                      variant="ghost"
                      size="icon"
                      className="text-white hover:bg-white/10 rounded-full w-12 h-12"
                      disabled={videoStatus.status !== 'completed'}
                    >
                      {isFullscreen ? <Minimize className="h-5 w-5" /> : <Maximize className="h-5 w-5" />}
                    </Button>
                  </div>

                  <Button 
                    className="bg-blue-600 hover:bg-blue-700 text-white rounded-xl px-6 shadow-lg shadow-blue-600/25"
                    onClick={handleDownload}
                    disabled={videoStatus.status !== 'completed'}
                  >
                    <Download className="mr-2 h-5 w-5" />
                    Download Video
                  </Button>
                </div>
              </div>
            )}
          </div>

          {/* Video Info */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="mt-8 grid md:grid-cols-3 gap-6"
          >
            <div className="bg-gradient-to-br from-gray-900/50 to-black/50 rounded-2xl p-6 border border-gray-800 backdrop-blur-sm">
              <h3 className="font-semibold text-white mb-2">Video Status</h3>
              <p className="text-gray-400 text-sm capitalize">{videoStatus.status}</p>
            </div>
            <div className="bg-gradient-to-br from-gray-900/50 to-black/50 rounded-2xl p-6 border border-gray-800 backdrop-blur-sm">
              <h3 className="font-semibold text-white mb-2">Topic</h3>
              <p className="text-gray-400 text-sm">{topic}</p>
            </div>
            <div className="bg-gradient-to-br from-gray-900/50 to-black/50 rounded-2xl p-6 border border-gray-800 backdrop-blur-sm">
              <h3 className="font-semibold text-white mb-2">Video ID</h3>
              <p className="text-gray-400 text-sm font-mono">{videoId || 'Not available'}</p>
            </div>
          </motion.div>
        </motion.div>
      </div>
      
      {/* Add fullscreen styles */}
      <style jsx global>{`
        .fullscreen-video {
          position: fixed !important;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          width: 100vw;
          height: 100vh;
          z-index: 9999;
          border-radius: 0 !important;
          border: none !important;
          display: flex;
          flex-direction: column;
        }
        
        .fullscreen-video > div:first-child {
          flex: 1;
          aspect-ratio: auto !important;
        }
      `}</style>
    </div>
  )
}

export default function VideoPage() {
  return (
    <Suspense
      fallback={
        <div className="min-h-screen bg-black flex items-center justify-center">
          <div className="text-white">Loading...</div>
        </div>
      }
    >
      <VideoPlayerContent />
    </Suspense>
  )
}
