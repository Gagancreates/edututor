"use client"

import { useState, useEffect, Suspense } from "react"
import { Button } from "@/components/ui/button"
import { ArrowLeft, Download, Play, Pause, Volume2, VolumeX, Share2, RotateCcw, Heart } from "lucide-react"
import { motion } from "framer-motion"
import Link from "next/link"
import { useSearchParams } from "next/navigation"

function VideoPlayerContent() {
  const searchParams = useSearchParams()
  const topic = searchParams.get("topic") || "Educational Topic"

  const [isPlaying, setIsPlaying] = useState(true)
  const [isMuted, setIsMuted] = useState(false)
  const [progress, setProgress] = useState(0)
  const [currentSubtitle, setCurrentSubtitle] = useState("")

  const subtitles = [
    "Welcome to this educational video about " + topic,
    "Let's explore the fundamental concepts together",
    "This visualization will help you understand the key principles",
    "Notice how the elements interact with each other",
    "This demonstrates the core theory in action",
  ]

  useEffect(() => {
    if (isPlaying) {
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
  }, [isPlaying, progress])

  const togglePlay = () => setIsPlaying(!isPlaying)
  const toggleMute = () => setIsMuted(!isMuted)

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
          <div className="relative bg-gradient-to-br from-gray-900 to-black rounded-3xl overflow-hidden border border-gray-800 shadow-2xl">
            {/* Video Canvas Area */}
            <div className="relative aspect-video bg-gradient-to-br from-blue-500/10 via-purple-500/10 to-cyan-500/10">
              {/* Simulated p5.js Animation */}
              <div className="absolute inset-0 flex items-center justify-center">
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
                  className="w-32 h-32 bg-gradient-to-br from-blue-400 to-purple-400 rounded-full opacity-60"
                />
                <motion.div
                  animate={{
                    scale: [1.2, 1, 1.2],
                    rotate: [360, 180, 0],
                  }}
                  transition={{
                    duration: 4,
                    repeat: Number.POSITIVE_INFINITY,
                    ease: "easeInOut",
                    delay: 1,
                  }}
                  className="absolute w-24 h-24 bg-gradient-to-br from-cyan-400 to-blue-400 rounded-full opacity-40"
                />
              </div>

              {/* Subtitles */}
              <div className="absolute bottom-0 left-0 right-0 p-6">
                <div className="bg-black/70 backdrop-blur-sm rounded-xl p-4 text-center">
                  <p className="text-white text-lg">{currentSubtitle}</p>
                </div>
              </div>

              {/* Play/Pause Overlay */}
              {!isPlaying && (
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

            {/* Controls */}
            <div className="p-6 bg-gradient-to-r from-gray-900/90 to-black/90 backdrop-blur-sm">
              {/* Progress Bar */}
              <div className="mb-4">
                <div className="flex items-center justify-between text-sm text-gray-400 mb-2">
                  <span>{Math.floor((progress / 100) * 120)}s</span>
                  <span>120s</span>
                </div>
                <div className="w-full bg-gray-700 rounded-full h-2 cursor-pointer">
                  <div
                    className="bg-gradient-to-r from-blue-500 to-purple-500 h-2 rounded-full transition-all duration-300"
                    style={{ width: `${progress}%` }}
                  />
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
                  >
                    {isPlaying ? <Pause className="h-6 w-6" /> : <Play className="h-6 w-6 ml-0.5" />}
                  </Button>

                  <Button
                    onClick={toggleMute}
                    variant="ghost"
                    size="icon"
                    className="text-white hover:bg-white/10 rounded-full w-12 h-12"
                  >
                    {isMuted ? <VolumeX className="h-5 w-5" /> : <Volume2 className="h-5 w-5" />}
                  </Button>

                  <Button
                    onClick={() => {
                      setProgress(0)
                      setIsPlaying(true)
                    }}
                    variant="ghost"
                    size="icon"
                    className="text-white hover:bg-white/10 rounded-full w-12 h-12"
                  >
                    <RotateCcw className="h-5 w-5" />
                  </Button>
                </div>

                <Button className="bg-blue-600 hover:bg-blue-700 text-white rounded-xl px-6 shadow-lg shadow-blue-600/25">
                  <Download className="mr-2 h-5 w-5" />
                  Download Video
                </Button>
              </div>
            </div>
          </div>

          {/* Video Info */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="mt-8 grid md:grid-cols-3 gap-6"
          >
            <div className="bg-gradient-to-br from-gray-900/50 to-black/50 rounded-2xl p-6 border border-gray-800 backdrop-blur-sm">
              <h3 className="font-semibold text-white mb-2">Video Quality</h3>
              <p className="text-gray-400 text-sm">1080p HD • 60fps</p>
            </div>
            <div className="bg-gradient-to-br from-gray-900/50 to-black/50 rounded-2xl p-6 border border-gray-800 backdrop-blur-sm">
              <h3 className="font-semibold text-white mb-2">Generation Time</h3>
              <p className="text-gray-400 text-sm">28 seconds</p>
            </div>
            <div className="bg-gradient-to-br from-gray-900/50 to-black/50 rounded-2xl p-6 border border-gray-800 backdrop-blur-sm">
              <h3 className="font-semibold text-white mb-2">AI Model</h3>
              <p className="text-gray-400 text-sm">EduTutor v2.0</p>
            </div>
          </motion.div>
        </motion.div>
      </div>
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
