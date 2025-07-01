"use client"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { ArrowRight, Github, Play, Sparkles, Brain, Zap, Users, BookOpen, TrendingUp, ChevronRight, Loader2, Menu, X } from "lucide-react"
import Link from "next/link"
import { motion, AnimatePresence } from "framer-motion"
import { useRouter } from "next/navigation"
import Image from "next/image"

export default function Home() {
  const [searchTopic, setSearchTopic] = useState("")
  const [isGenerating, setIsGenerating] = useState(false)
  const [generationStep, setGenerationStep] = useState(0)
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const [isMobile, setIsMobile] = useState(true)
  const router = useRouter()
  
  useEffect(() => {
    const checkMobile = () => {
      setIsMobile(window.innerWidth < 640);
    };
    
    // Initial check
    checkMobile();
    
    // Add event listener
    window.addEventListener('resize', checkMobile);
    
    // Cleanup
    return () => window.removeEventListener('resize', checkMobile);
  }, []);
  
  const generationSteps = [
    { icon: Brain, title: "Analyzing Topic", description: "Understanding the educational concept" },
    { icon: Sparkles, title: "Creating Animations", description: "Generating custom p5.js visualizations" },
    { icon: Zap, title: "Synthesizing Voice", description: "Creating natural AI narration" },
    { icon: Play, title: "Finalizing Video", description: "Combining all elements together" },
  ]
  
  const handleGenerate = () => {
    if (!searchTopic.trim()) return
    
    setIsGenerating(true)
    setGenerationStep(0)
    
    // Simulate generation process with step progression
    const stepInterval = setInterval(() => {
      setGenerationStep((prev) => {
        if (prev >= 3) {
          clearInterval(stepInterval)
          setTimeout(() => {
            // Navigate to video player page
            router.push(`/video?topic=${encodeURIComponent(searchTopic)}`)
          }, 1000)
          return prev
        }
        return prev + 1
      })
    }, 2000)
  }
  return (
    <div 
      className="min-h-screen relative overflow-hidden font-inter bg-black"
    >
      {/* Background container */}
      
      <header className="relative z-20 container mx-auto px-4 sm:px-6 py-4 sm:py-6 flex items-center justify-between">
        <motion.div 
          initial={{ opacity: 1, x: -20 }} 
          animate={{ opacity: 1, x: 0 }} 
          transition={{ duration: 0.6, ease: "easeOut" }}
          className="flex items-center gap-2 sm:gap-3"
        >
          <div className="relative group">
            <div className="size-10 sm:size-12 rounded-2xl bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center shadow-lg shadow-blue-500/25 transition-all duration-300 group-hover:shadow-xl group-hover:shadow-blue-500/30 relative overflow-hidden">
              <Image src="/images/v4.png" alt="EduTutor Logo" fill style={{objectFit: 'contain'}} />
            </div>
            <div className="absolute inset-0 rounded-2xl bg-gradient-to-br from-blue-500 to-purple-600 blur-md opacity-50 -z-10 transition-all duration-300 group-hover:opacity-70 group-hover:blur-lg" />
          </div>
          <span className="font-bold text-xl sm:text-3xl text-white tracking-tight">EduTutor</span>
        </motion.div>

        {/* Mobile menu button */}
        <div className="md:hidden">
          <Button 
            variant="ghost" 
            size="icon" 
            className="text-gray-300 hover:text-white hover:bg-white/10 rounded-xl transition-all duration-300"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          >
            {mobileMenuOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
          </Button>
        </div>

        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2, ease: "easeOut" }}
          className="hidden md:flex items-center gap-10"
        >
          <Link href="#features" className="text-gray-300 hover:text-white font-medium transition-colors">
            Features
          </Link>
          <Link href="#transform" className="text-gray-300 hover:text-white font-medium transition-colors">
            Transform
          </Link>
          <Link href="#impact" className="text-gray-300 hover:text-white font-medium transition-colors">
            Impact
          </Link>
        </motion.div>

        <motion.div 
          initial={{ opacity: 0, x: 20 }} 
          animate={{ opacity: 1, x: 0 }} 
          transition={{ duration: 0.6, delay: 0.3, ease: "easeOut" }}
          className="hidden md:flex items-center gap-4"
        >
          <Link href="https://github.com" target="_blank">
            <Button variant="ghost" size="icon" className="text-gray-400 hover:text-white hover:bg-white/10 rounded-xl transition-all duration-300">
              <Github className="h-5 w-5" />
            </Button>
          </Link>
          <Button className="bg-blue-600 hover:bg-blue-500 text-white rounded-xl px-6 shadow-lg shadow-blue-600/25 border border-blue-500/20 transition-all duration-300 hover:shadow-xl hover:shadow-blue-600/30">
            Get Started
          </Button>
        </motion.div>
      </header>

      {/* Mobile Menu */}
      <AnimatePresence>
        {mobileMenuOpen && (
          <motion.div 
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.3 }}
            className="md:hidden absolute top-16 left-0 right-0 z-30 bg-gradient-to-b from-gray-900 to-black border-b border-gray-800 py-4 px-6"
          >
            <div className="flex flex-col space-y-4">
              <Link href="#features" className="text-gray-300 hover:text-white font-medium transition-colors py-2">
                Features
              </Link>
              <Link href="#transform" className="text-gray-300 hover:text-white font-medium transition-colors py-2">
                Transform
              </Link>
              <Link href="#impact" className="text-gray-300 hover:text-white font-medium transition-colors py-2">
                Impact
              </Link>
              <div className="pt-2 flex items-center gap-4">
                <Link href="https://github.com" target="_blank">
                  <Button variant="ghost" size="icon" className="text-gray-400 hover:text-white hover:bg-white/10 rounded-xl transition-all duration-300">
                    <Github className="h-5 w-5" />
                  </Button>
                </Link>
                <Button className="bg-blue-600 hover:bg-blue-500 text-white rounded-xl px-6 shadow-lg shadow-blue-600/25 border border-blue-500/20 transition-all duration-300 hover:shadow-xl hover:shadow-blue-600/30">
                  Get Started
                </Button>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      <main className="relative z-10">
        <>
          {/* Hero Section - Optimized for mobile and desktop */}
          <section className="container mx-auto px-4 sm:px-6 min-h-[calc(100vh-5rem)] flex flex-col justify-center pt-4 relative overflow-hidden">
            {/* Full-width grid background with fade-out effect - Fixed to viewport */}
            <div className="fixed left-0 right-0 top-0 w-[100vw] h-[calc(100vh+45rem)] -z-10 overflow-hidden">
              {/* Base grid pattern with slightly increased opacity */}
              <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.14)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.14)_1px,transparent_1px)] bg-[size:30px_30px]"></div>
              
              {/* Radial mask that creates the gradient effect - transparent in center, darker at edges */}
              <div className="absolute inset-x-0 top-0 h-[50%] bg-radial-mask"></div>
              
              {/* Strong bottom fade-out effect precisely positioned to end before videos section */}
              <div className="absolute left-0 right-0 bottom-0 h-[25%] bg-gradient-to-t from-black via-black/90 to-transparent"></div>
              
              {/* Additional strong fade for precise cutoff */}
              <div className="absolute left-0 right-0 bottom-0 h-[5rem] bg-black"></div>
            </div>
            
            {/* Content area with protective layer to improve text readability */}
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, ease: "easeOut" }}
              className="max-w-5xl mx-auto text-center relative z-10"
            >
              {/* Subtle backdrop for improved text contrast - without blur */}
              <div className="absolute inset-0 -z-10 bg-black/20 rounded-3xl transform scale-110"></div>
              
              <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.2, duration: 0.7 }}
                className="inline-flex items-center gap-1 sm:gap-2 bg-blue-500/20 border border-blue-500/30 rounded-full px-3 sm:px-6 py-1.5 sm:py-3 mb-4 sm:mb-8"
              >
                <Sparkles className="h-3 w-3 sm:h-4 sm:w-4 text-blue-400" />
                <span className="text-blue-300 text-xs sm:text-sm font-medium">Revolutionizing Education with AI</span>
              </motion.div>

              <h1 className="font-bold text-3xl sm:text-5xl md:text-6xl lg:text-7xl text-white mb-4 sm:mb-8 leading-tight tracking-tight relative aesthetic-text">
                <span className="absolute -inset-1 bg-gradient-to-tr from-purple-500/5 to-blue-500/5 rounded-3xl blur-3xl -z-10"></span>
                Your Personal{" "}
                <span className="bg-clip-text text-transparent drop-shadow-sm animate-text-shimmer ai-tutor-text inline-block">
                  AI Video Tutor
                </span>
              </h1>

              <p className="text-base sm:text-xl md:text-2xl text-gray-300 mb-6 sm:mb-10 max-w-3xl mx-auto leading-relaxed tracking-wide aesthetic-text px-1">
                Learn anything, smarter. Personalized video lessons, powered by AI.
              </p>

              <AnimatePresence mode="wait">
                {!isGenerating ? (
                  <motion.div
                    key="input"
                    initial={{ opacity: 0, y: 30 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -30 }}
                  >
                    <div className="max-w-2xl mx-auto mb-6 sm:mb-8 relative">
                      {/* Silver glow background */}
                      <div className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-32 sm:w-[36rem] sm:h-40 bg-[radial-gradient(ellipse_at_center,_rgba(192,192,192,0.45)_0%,_rgba(192,192,192,0.15)_60%,_transparent_100%)] blur-2xl z-0 pointer-events-none" />
                      <div className="relative group z-10">
                        <Input
                          placeholder={isMobile ? 
                            "What would you like to learn today?" : 
                            "What would you like to learn today? e.g. Explain me Quadratic Equations..."}
                          className="h-18 sm:h-20 md:h-20 text-base lg:text-base sm:text-xl rounded-2xl sm:rounded-3xl border-2 border-gray-600 bg-gray-900/60 text-white placeholder-gray-400 focus:border-blue-500 focus:ring-blue-500 backdrop-blur-sm px-4 sm:px-8 shadow-lg transition-all duration-300 focus:border-blue-500/70 md:placeholder:pt- md:placeholder:leading-tight"
                          value={searchTopic}
                          onChange={(e) => setSearchTopic(e.target.value)}
                          onKeyPress={(e) => {
                            if (e.key === "Enter" && searchTopic.trim()) {
                              handleGenerate();
                            }
                          }}
                        />
                        {/* Enhanced glow effect */}
                        <div className="absolute inset-0 rounded-2xl sm:rounded-3xl bg-gradient-to-r from-blue-500/20 to-purple-500/20 blur-xl -z-10 opacity-40 group-hover:opacity-60 transition-opacity duration-300" />
                        {/* Enhanced animated glow border */}
                        <div className="absolute inset-0 -z-10 rounded-2xl sm:rounded-3xl opacity-30 group-hover:opacity-60 transition-opacity duration-300">
                          <div className="absolute inset-0 bg-gradient-to-r from-blue-500/30 via-purple-500/40 to-blue-500/30 bg-[length:200%_100%] rounded-2xl sm:rounded-3xl animate-glow"></div>
                        </div>
                        {/* Sparkle icon inside input */}
                        <div className="absolute right-4 sm:right-6 top-1/2 -translate-y-1/2 text-blue-400/50 group-hover:text-blue-400/70 transition-colors duration-300">
                          <Sparkles className="h-5 w-5 sm:h-6 sm:w-6" />
                        </div>
                      </div>
                    </div>

                    <div className="flex flex-col sm:flex-row gap-3 sm:gap-6 justify-center items-center mb-6 sm:mb-12 px-2 sm:px-0">
                      <div className="w-full sm:w-auto relative">
                        {/* Extra div with solid background for disabled state */}
                        <div className={`absolute inset-0 ${searchTopic.trim() ? 'bg-blue-600' : 'bg-blue-600/50'} rounded-xl sm:rounded-2xl transition-colors duration-300`}></div>
                        <Button 
                          className="w-full sm:w-auto bg-transparent hover:bg-blue-500 text-white rounded-xl sm:rounded-2xl h-12 sm:h-14 md:h-16 px-4 sm:px-8 md:px-10 text-sm sm:text-lg font-semibold shadow-xl sm:shadow-2xl shadow-blue-600/25 border border-blue-500/20 group transition-all duration-300 hover:shadow-xl hover:shadow-blue-600/30 relative overflow-hidden disabled:opacity-70 disabled:shadow-lg disabled:shadow-blue-600/10"
                          onClick={handleGenerate}
                          disabled={!searchTopic.trim()}
                        >
                          <span className="absolute inset-0 bg-gradient-to-r from-blue-500/0 via-blue-500/30 to-blue-500/0 opacity-0 group-hover:opacity-100 transition-opacity duration-500 -z-10 animate-text-shimmer"></span>
                          <Sparkles className={`mr-2 sm:mr-3 h-4 w-4 sm:h-5 sm:w-5 ${!searchTopic.trim() ? 'opacity-70' : 'opacity-100'} transition-opacity duration-300`} />
                          <span className={`aesthetic-text ${!searchTopic.trim() ? 'opacity-70' : 'opacity-100'} transition-opacity duration-300`}>Generate Video</span>
                        </Button>
                      </div>
                      
                      <div className="w-full sm:w-auto relative">
                        {/* Extra div with solid background for demo button */}
                        <div className="absolute inset-0 bg-black/60 rounded-xl sm:rounded-2xl"></div>
                        <Button
                          variant="ghost"
                          className="w-full sm:w-auto text-gray-300 hover:text-white hover:bg-white/10 rounded-xl sm:rounded-2xl h-12 sm:h-14 md:h-16 px-4 sm:px-8 md:px-10 text-sm sm:text-lg border border-gray-700 transition-all duration-300 aesthetic-text relative overflow-hidden"
                          onClick={() => window.location.href = '#videos'}
                        >
                          <Play className="mr-2 sm:mr-3 h-4 w-4 sm:h-5 sm:w-5" />
                          Watch Demo
                        </Button>
                      </div>
                    </div>
                    
                    <div className="mt-4 sm:mt-8 w-full mx-auto relative py-2 sm:py-6">
                      <p className="text-gray-400 text-xs sm:text-sm mb-2 sm:mb-4 text-center">Try asking about...</p>
                      
                      {/* Container with masks for fading effect */}
                      <div className="relative w-full overflow-hidden h-16 sm:h-24">
                        {/* Left fade mask */}
                        <div className="absolute left-0 top-0 w-6 sm:w-20 h-full z-10 bg-gradient-to-r from-black to-transparent pointer-events-none"></div>
                        
                        {/* Right fade mask */}
                        <div className="absolute right-0 top-0 w-6 sm:w-20 h-full z-10 bg-gradient-to-l from-black to-transparent pointer-events-none"></div>
                        
                        {/* First row - moving left to right */}
                        <div className="relative w-full h-8 sm:h-10 mb-2 sm:mb-4 overflow-hidden">
                          <motion.div 
                            className="flex gap-1 sm:gap-4 absolute"
                            animate={{ 
                              x: ["-100%", "0%"], 
                            }}
                            transition={{ 
                              x: {
                                repeat: Infinity,
                                repeatType: "loop",
                                duration: 40,
                                ease: "linear"
                              }
                            }}
                          >
                            {[
                              "Explain quadratic equations",
                              "What is photosynthesis?",
                              "How do neurons work?",
                              "Explain the water cycle",
                              "What is the Big Bang theory?",
                              "How does blockchain work?",
                              "Explain Laplace transforms",
                              "What is mitosis?",
                            ].map((example, index) => (
                              <motion.button
                                key={index}
                                className="p-1.5 sm:p-3 rounded-lg sm:rounded-xl border border-gray-700 bg-gray-900/60 hover:bg-gray-800/70 text-gray-300 hover:text-white transition-all text-xs sm:text-sm whitespace-nowrap"
                                whileHover={{ scale: 1.05, borderColor: "rgba(96, 165, 250, 0.5)" }}
                                onClick={() => setSearchTopic(example)}
                              >
                                {example}
                              </motion.button>
                            ))}
                          </motion.div>

                          {/* Duplicate first row for seamless loop */}
                          <motion.div 
                            className="flex gap-1 sm:gap-4 absolute"
                            animate={{ 
                              x: ["0%", "100%"], 
                            }}
                            transition={{ 
                              x: {
                                repeat: Infinity,
                                repeatType: "loop",
                                duration: 40,
                                ease: "linear"
                              }
                            }}
                          >
                            {[
                              "Explain quadratic equations",
                              "What is photosynthesis?",
                              "How do neurons work?",
                              "Explain the water cycle",
                              "What is the Big Bang theory?",
                              "How does blockchain work?",
                              "Explain Laplace transforms",
                              "What is mitosis?",
                            ].map((example, index) => (
                              <motion.button
                                key={index}
                                className="p-1.5 sm:p-3 rounded-lg sm:rounded-xl border border-gray-700 bg-gray-900/60 hover:bg-gray-800/70 text-gray-300 hover:text-white transition-all text-xs sm:text-sm whitespace-nowrap"
                                whileHover={{ scale: 1.05, borderColor: "rgba(96, 165, 250, 0.5)" }}
                                onClick={() => setSearchTopic(example)}
                              >
                                {example}
                              </motion.button>
                            ))}
                          </motion.div>
                        </div>
                        
                        {/* Second row - moving right to left, with different examples */}
                        <div className="relative w-full h-8 sm:h-10 overflow-hidden">
                          <motion.div 
                            className="flex gap-1 sm:gap-4 absolute"
                            animate={{ 
                              x: ["0%", "-100%"], 
                            }}
                            transition={{ 
                              x: {
                                repeat: Infinity,
                                repeatType: "loop",
                                duration: 40,
                                ease: "linear"
                              }
                            }}
                          >
                            {[
                              "What caused the French Revolution?",
                              "How do vaccines work?",
                              "Explain quantum entanglement",
                              "What is machine learning?",
                              "How do black holes form?",
                              "Explain the theory of relativity",
                              "What is DNA replication?",
                              "How does the internet work?",
                              "What is the Pythagorean theorem?",
                            ].map((example, index) => (
                              <motion.button
                                key={index}
                                className="p-1.5 sm:p-3 rounded-lg sm:rounded-xl border border-gray-700 bg-gray-900/60 hover:bg-gray-800/70 text-gray-300 hover:text-white transition-all text-xs sm:text-sm whitespace-nowrap"
                                whileHover={{ scale: 1.05, borderColor: "rgba(124, 58, 237, 0.5)" }}
                                onClick={() => setSearchTopic(example)}
                              >
                                {example}
                              </motion.button>
                            ))}
                          </motion.div>

                          {/* Duplicate second row for seamless loop */}
                          <motion.div 
                            className="flex gap-1 sm:gap-4 absolute"
                            animate={{ 
                              x: ["100%", "0%"], 
                            }}
                            transition={{ 
                              x: {
                                repeat: Infinity,
                                repeatType: "loop",
                                duration: 40,
                                ease: "linear"
                              }
                            }}
                          >
                            {[
                              "What caused the French Revolution?",
                              "How do vaccines work?",
                              "Explain quantum entanglement",
                              "What is machine learning?",
                              "How do black holes form?",
                              "Explain the theory of relativity",
                              "What is DNA replication?",
                              "How does the internet work?",
                              "What is the Pythagorean theorem?",
                            ].map((example, index) => (
                              <motion.button
                                key={index}
                                className="p-1.5 sm:p-3 rounded-lg sm:rounded-xl border border-gray-700 bg-gray-900/60 hover:bg-gray-800/70 text-gray-300 hover:text-white transition-all text-xs sm:text-sm whitespace-nowrap"
                                whileHover={{ scale: 1.05, borderColor: "rgba(124, 58, 237, 0.5)" }}
                                onClick={() => setSearchTopic(example)}
                              >
                                {example}
                              </motion.button>
                            ))}
                          </motion.div>
                        </div>
                      </div>
                    </div>
                  </motion.div>
                ) : null}
              </AnimatePresence>
              
              {/* Modal Overlay for Video Generation */}
              <AnimatePresence>
                {isGenerating && (
                  <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    className="fixed inset-0 flex items-center justify-center z-50"
                  >
                    {/* Backdrop with blur */}
                    <motion.div
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      exit={{ opacity: 0 }}
                      className="absolute inset-0 bg-black/80"
                      onClick={() => setIsGenerating(false)}
                    />
                    
                    {/* Modal Content */}
                    <motion.div
                      key="generating-modal"
                      initial={{ opacity: 0, scale: 0.9, y: 20 }}
                      animate={{ opacity: 1, scale: 1, y: 0 }}
                      exit={{ opacity: 0, scale: 0.95, y: 10 }}
                      className="relative bg-gradient-to-br from-gray-900/90 to-black/90 rounded-3xl border border-gray-700 p-8 md:p-12 text-center max-w-4xl mx-auto shadow-2xl z-10 overflow-hidden"
                    >
                      {/* Decorative elements */}
                      <div className="absolute top-0 left-0 w-full h-full bg-[linear-gradient(rgba(79,70,229,0.03)_1px,transparent_1px),linear-gradient(90deg,rgba(79,70,229,0.03)_1px,transparent_1px)] bg-[size:30px_30px] opacity-20" />
                      <div className="absolute -top-40 -right-40 w-80 h-80 bg-blue-500/5 rounded-full blur-3xl" />
                      <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-purple-500/5 rounded-full blur-3xl" />
                      
                      <div className="relative">
                        <h2 className="font-bold text-3xl md:text-4xl text-white mb-4">Creating Your Educational Video</h2>
                        <p className="text-xl text-gray-300 mb-12">
                          Topic: <span className="text-blue-400">{searchTopic}</span>
                        </p>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-12">
                          {generationSteps.map((step, index) => {
                            const isActive = index === generationStep
                            const isCompleted = index < generationStep
                            const IconComponent = step.icon

                            return (
                              <motion.div
                                key={index}
                                initial={{ opacity: 0.3, scale: 0.95 }}
                                animate={{
                                  opacity: isActive ? 1 : isCompleted ? 0.8 : 0.3,
                                  scale: isActive ? 1.05 : 1,
                                }}
                                className={`relative p-6 rounded-2xl border transition-all duration-500 ${
                                  isActive
                                    ? "border-blue-500 bg-blue-500/10"
                                    : isCompleted
                                      ? "border-green-500 bg-green-500/10"
                                      : "border-gray-700 bg-gray-900/30"
                                }`}
                              >
                                <div className="flex items-center gap-4">
                                  <div
                                    className={`size-12 rounded-xl flex items-center justify-center ${
                                      isActive
                                        ? "bg-blue-500/20 border border-blue-500/30"
                                        : isCompleted
                                          ? "bg-green-500/20 border border-green-500/30"
                                          : "bg-gray-700/20 border border-gray-600/30"
                                    }`}
                                  >
                                    {isActive ? (
                                      <Loader2 className="h-6 w-6 text-blue-400 animate-spin" />
                                    ) : (
                                      <IconComponent
                                        className={`h-6 w-6 ${isCompleted ? "text-green-400" : "text-gray-400"}`}
                                      />
                                    )}
                                  </div>
                                  <div className="text-left">
                                    <h3
                                      className={`font-semibold text-lg ${
                                        isActive ? "text-blue-400" : isCompleted ? "text-green-400" : "text-gray-400"
                                      }`}
                                    >
                                      {step.title}
                                    </h3>
                                    <p className="text-gray-300 text-sm">{step.description}</p>
                                  </div>
                                </div>

                                {isActive && (
                                  <motion.div
                                    initial={{ width: "0%" }}
                                    animate={{ width: "100%" }}
                                    transition={{ duration: 2 }}
                                    className="absolute bottom-0 left-0 h-1 bg-gradient-to-r from-blue-500 to-purple-500 rounded-b-2xl"
                                  />
                                )}
                              </motion.div>
                            )
                          })}
                        </div>

                        <motion.div
                          initial={{ opacity: 0 }}
                          animate={{ opacity: 1 }}
                          transition={{ delay: 0.5 }}
                          className="bg-gradient-to-br from-gray-900/70 to-black/70 rounded-2xl p-8 border border-gray-800 backdrop-blur-sm mb-8"
                        >
                          <div className="flex items-center justify-center gap-3 mb-4">
                            <Loader2 className="h-6 w-6 text-blue-400 animate-spin" />
                            <span className="text-white font-medium">Processing...</span>
                          </div>
                          <div className="w-full bg-gray-700/50 rounded-full h-2">
                            <motion.div
                              initial={{ width: "0%" }}
                              animate={{ width: `${((generationStep + 1) / generationSteps.length) * 100}%` }}
                              transition={{ duration: 0.5 }}
                              className="bg-gradient-to-r from-blue-500 to-purple-500 h-2 rounded-full"
                            />
                          </div>
                          <p className="text-gray-400 text-sm mt-4 text-center">
                            This usually takes 20-30 seconds. We're creating something amazing for you!
                          </p>
                        </motion.div>
                        
                        <Button
                          variant="outline"
                          className="text-gray-300 hover:text-white border-gray-600 hover:bg-gray-800/50"
                          onClick={() => setIsGenerating(false)}
                        >
                          Cancel
                        </Button>
                      </div>
                    </motion.div>
                  </motion.div>
                )}
              </AnimatePresence>
              
              {/* Scroll indicator */}
              <motion.div 
                initial={{ opacity: 0, y: 10 }} 
                animate={{ opacity: 1, y: 0 }} 
                transition={{ delay: 1.2, duration: 0.8 }}
                className="hidden md:flex flex-col items-center mt-4 gap-2"
              >
                
              </motion.div>
            </motion.div>



            {/* Generated Videos Gallery */}
            <motion.div
              initial={{ opacity: 0, y: 40 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.8 }}
              className="mt-40 relative"
              id="videos"
            >
              <div className="bg-gradient-to-br from-gray-900/50 to-black/50 rounded-3xl border border-gray-800 shadow-2xl backdrop-blur-sm overflow-hidden">
                <div className="p-8 md:p-12">
                  <div className="flex justify-between items-center mb-8">
                    <h3 className="text-2xl font-bold text-white">Recently Generated Videos</h3>
                    <Button variant="ghost" className="text-blue-400 hover:text-blue-300">
                      View All <ArrowRight className="ml-2 h-4 w-4" />
                    </Button>
                  </div>
                  
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    {[
                      { title: "Quantum Physics Basics", duration: "5:24", views: "2.4K", thumbnail: "/images/quantum.jpg" },
                      { title: "Introduction to Neural Networks", duration: "8:15", views: "1.8K", thumbnail: "/images/neural.jpg" },
                      { title: "Ancient Roman History", duration: "6:42", views: "3.2K", thumbnail: "/images/rome.jpg" },
                      { title: "Climate Change Effects", duration: "7:30", views: "4.5K", thumbnail: "/images/climate.jpg" },
                      { title: "Introduction to Calculus", duration: "9:18", views: "2.1K", thumbnail: "/images/calculus.jpg" },
                      { title: "Solar System Exploration", duration: "4:55", views: "5.7K", thumbnail: "/images/solar.jpg" },
                    ].map((video, index) => (
                      <motion.div
                        key={index}
                        initial={{ opacity: 0, y: 20 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        viewport={{ once: true }}
                        transition={{ delay: index * 0.1, duration: 0.5 }}
                        className="group relative cursor-pointer"
                      >
                        <div className="aspect-video rounded-xl overflow-hidden bg-gradient-to-br from-blue-500/20 to-purple-500/20 border border-gray-800 group-hover:border-blue-500/30 transition-all duration-300">
                          <div className="absolute inset-0 flex items-center justify-center">
                            <div className="relative size-16 bg-black/40 rounded-full flex items-center justify-center backdrop-blur-sm border border-white/10 opacity-80 group-hover:opacity-100 transition-all duration-300 group-hover:bg-blue-500/20">
                              <Play className="h-6 w-6 text-white ml-1" />
                            </div>
                          </div>
                          <div className="absolute bottom-0 left-0 right-0 p-4 bg-gradient-to-t from-black/80 to-transparent">
                            <h4 className="text-white font-medium text-lg mb-1 line-clamp-1">{video.title}</h4>
                            <div className="flex items-center gap-3 text-sm text-gray-300">
                              <span>{video.duration}</span>
                              <span>•</span>
                              <span>{video.views} views</span>
                            </div>
                          </div>
                    </div>
                      </motion.div>
                    ))}
                  </div>
                </div>
              </div>
            </motion.div>

            {/* Stats */}
            <motion.div
              initial={{ opacity: 0, y: 40 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.8 }}
              className="grid grid-cols-2 md:grid-cols-4 gap-8 mt-24 max-w-4xl mx-auto"
            >
              {[
                { number: "10K+", label: "Videos Created" },
                { number: "50K+", label: "Students Reached" },
                { number: "95%", label: "Engagement Rate" },
                { number: "30s", label: "Average Creation Time" },
              ].map((stat, index) => (
                <div key={index} className="text-center relative group">
                  <div className="absolute inset-0 bg-blue-500/5 rounded-xl opacity-0 group-hover:opacity-100 transition-opacity duration-300 -z-10" />
                  <div className="text-3xl md:text-4xl font-bold text-white mb-2">{stat.number}</div>
                  <div className="text-gray-400 text-sm">{stat.label}</div>
                </div>
              ))}
            </motion.div>
          </section>

          {/* Transform Education Section */}
          <section id="transform" className="container mx-auto px-6 py-28">
            <motion.div
              initial={{ opacity: 0 }}
              whileInView={{ opacity: 1 }}
              viewport={{ once: true, margin: "-100px" }}
              transition={{ duration: 0.8 }}
              className="text-center mb-24"
            >
              <h2 className="font-bold text-4xl md:text-6xl text-white mb-8 [text-shadow:0_0_25px_rgba(79,70,229,0.15)] relative">
                <span className="absolute -inset-1 bg-gradient-to-tr from-purple-500/5 to-blue-500/5 rounded-3xl blur-3xl -z-10"></span>
                Transforming Education,{" "}
                <span className="bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent drop-shadow-sm">
                  One Video at a Time
                </span>
              </h2>
              <p className="text-xl text-gray-300 max-w-3xl mx-auto tracking-wide">
                From traditional textbooks to immersive visual experiences. See how EduTutor is revolutionizing the
                way we learn and teach.
              </p>
            </motion.div>

            <div className="grid md:grid-cols-2 gap-16 items-center">
              <motion.div
                initial={{ opacity: 0, x: -50 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true, margin: "-100px" }}
                transition={{ duration: 0.8 }}
                className="space-y-10"
              >
                {[
                  {
                    icon: BookOpen,
                    title: "From Static to Dynamic",
                    description:
                      "Transform boring textbook concepts into engaging visual narratives that students actually want to watch.",
                  },
                  {
                    icon: Brain,
                    title: "AI-Powered Personalization",
                    description:
                      "Every video is uniquely crafted to match the learning style and pace of your students.",
                  },
                  {
                    icon: TrendingUp,
                    title: "Measurable Impact",
                    description:
                      "See 3x higher engagement rates and 40% better retention compared to traditional methods.",
                  },
                ].map((item, index) => (
                  <motion.div 
                    key={index} 
                    className="flex gap-5 group"
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    transition={{ delay: index * 0.2, duration: 0.6 }}
                  >
                    <div className="flex-shrink-0">
                      <div className="size-14 rounded-xl bg-gradient-to-br from-blue-500/20 to-purple-500/20 border border-blue-500/20 flex items-center justify-center backdrop-blur-sm group-hover:border-blue-500/40 transition-all duration-300">
                        <item.icon className="h-7 w-7 text-blue-400" />
                      </div>
                    </div>
                    <div>
                      <h3 className="font-bold text-2xl text-white mb-3">{item.title}</h3>
                      <p className="text-gray-300 leading-relaxed">{item.description}</p>
                    </div>
                  </motion.div>
                ))}
              </motion.div>

              <motion.div
                initial={{ opacity: 0, x: 50 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true, margin: "-100px" }}
                transition={{ duration: 0.8 }}
                className="relative"
              >
                <div className="absolute inset-0 bg-gradient-to-br from-blue-500/10 to-purple-500/10 rounded-3xl blur-xl -z-10" />
                <div className="relative bg-gradient-to-br from-gray-900 to-black rounded-3xl p-8 border border-gray-800 shadow-2xl overflow-hidden group hover:border-gray-700 transition-all duration-500">
                  <div className="absolute inset-0 bg-gradient-to-br from-blue-500/5 to-purple-500/5 rounded-3xl" />
                  <div className="relative">
                    <div className="flex items-center gap-3 mb-8">
                      <div className="flex gap-2">
                        <div className="size-3 rounded-full bg-red-500" />
                        <div className="size-3 rounded-full bg-yellow-500" />
                        <div className="size-3 rounded-full bg-green-500" />
                      </div>
                      <span className="text-gray-400 text-sm">EduTutor Studio</span>
                    </div>
                    <div className="space-y-5">
                      <div className="h-4 bg-gradient-to-r from-blue-500 to-transparent rounded-full w-3/4" />
                      <div className="h-4 bg-gradient-to-r from-purple-500 to-transparent rounded-full w-1/2" />
                      <div className="h-4 bg-gradient-to-r from-cyan-500 to-transparent rounded-full w-2/3" />
                      <div className="mt-10 aspect-video bg-gradient-to-br from-blue-500/20 to-purple-500/20 rounded-xl border border-blue-500/20 flex items-center justify-center overflow-hidden group-hover:border-blue-500/30 transition-all duration-300">
                        <div className="relative size-20 bg-white/10 rounded-full flex items-center justify-center backdrop-blur-sm border border-white/20 group-hover:bg-white/20 transition-all duration-300">
                          <Play className="h-8 w-8 text-white ml-1" />
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </motion.div>
            </div>
          </section>

          {/* Features Grid */}
          <section id="features" className="container mx-auto px-6 py-28 relative">
            {/* Decorative grid for this section */}
            <div className="absolute inset-0 bg-[linear-gradient(rgba(79,70,229,0.02)_1px,transparent_1px),linear-gradient(90deg,rgba(79,70,229,0.02)_1px,transparent_1px)] bg-[size:40px_40px] opacity-60" />
            
            <motion.div
              initial={{ opacity: 0 }}
              whileInView={{ opacity: 1 }}
              viewport={{ once: true, margin: "-100px" }}
              transition={{ duration: 0.8 }}
              className="text-center mb-24 relative"
            >
              <div className="absolute -top-10 left-1/2 -translate-x-1/2 w-40 h-40 bg-blue-500/5 rounded-full blur-3xl" />
              <h2 className="font-bold text-4xl md:text-6xl text-white mb-8 [text-shadow:0_0_25px_rgba(79,70,229,0.15)] relative">
                <span className="absolute -inset-1 bg-gradient-to-tr from-purple-500/5 to-blue-500/5 rounded-3xl blur-3xl -z-10"></span>
                Powered by Next-Gen AI
              </h2>
              <p className="text-xl text-gray-300 max-w-2xl mx-auto tracking-wide">
                Every feature designed to make education more engaging, accessible, and effective.
              </p>
            </motion.div>

            <div className="grid md:grid-cols-3 gap-8 relative z-10">
              {[
                {
                  icon: Zap,
                  title: "Lightning Fast Generation",
                  description:
                    "Create professional educational videos in under 30 seconds with our advanced AI pipeline.",
                  gradient: "from-yellow-500 to-orange-500",
                },
                {
                  icon: Brain,
                  title: "Intelligent Animations",
                  description:
                    "AI analyzes your topic and creates custom p5.js animations that perfectly illustrate concepts.",
                  gradient: "from-blue-500 to-purple-500",
                },
                {
                  icon: Users,
                  title: "Natural Voice Synthesis",
                  description:
                    "Human-like narration that adapts tone and pace to match the complexity of your content.",
                  gradient: "from-green-500 to-cyan-500",
                },
              ].map((feature, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 30 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true, margin: "-100px" }}
                  transition={{ delay: index * 0.2, duration: 0.7 }}
                  className="group relative"
                >
                  <div className="absolute inset-0 bg-gradient-to-br from-white/5 to-transparent rounded-3xl opacity-0 group-hover:opacity-100 transition-all duration-500" />
                  <div className="relative bg-gradient-to-br from-gray-900/50 to-black/50 rounded-3xl p-10 border border-gray-800 backdrop-blur-sm hover:border-gray-700 transition-all duration-500 h-full">
                    <div
                      className={`size-16 rounded-2xl bg-gradient-to-br ${feature.gradient} flex items-center justify-center mb-8 group-hover:shadow-lg transition-all duration-300 relative`}
                    >
                      <div className={`absolute inset-0 bg-gradient-to-br ${feature.gradient} rounded-2xl blur opacity-40 group-hover:opacity-60 transition-opacity duration-300`} />
                      <feature.icon className="h-8 w-8 text-white relative z-10" />
                    </div>
                    <h3 className="font-bold text-2xl text-white mb-4">{feature.title}</h3>
                    <p className="text-gray-300 leading-relaxed">{feature.description}</p>
                    
                    <div className="mt-8 opacity-0 group-hover:opacity-100 transition-all duration-500 transform translate-y-2 group-hover:translate-y-0">
                      <Link href="#" className="text-blue-400 flex items-center text-sm font-medium hover:text-blue-300 transition-colors">
                        Learn more
                        <ChevronRight className="h-4 w-4 ml-1" />
                      </Link>
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>
          </section>

          {/* Testimonials */}
          <section className="container mx-auto px-6 py-28 relative">
            {/* Decorative background for testimonials */}
            <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,rgba(79,70,229,0.05),transparent_50%)] opacity-70" />
            
            <motion.div
              initial={{ opacity: 0 }}
              whileInView={{ opacity: 1 }}
              viewport={{ once: true, margin: "-100px" }}
              transition={{ duration: 0.8 }}
              className="text-center mb-20 relative"
            >
              <div className="absolute -top-10 left-1/2 -translate-x-1/2 w-40 h-40 bg-purple-500/5 rounded-full blur-3xl" />
              <h2 className="font-bold text-4xl md:text-6xl text-white mb-8 [text-shadow:0_0_25px_rgba(79,70,229,0.15)] relative">
                <span className="absolute -inset-1 bg-gradient-to-tr from-purple-500/5 to-blue-500/5 rounded-3xl blur-3xl -z-10"></span>
                Trusted by Educators <span className="bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent drop-shadow-sm">Worldwide</span>
              </h2>
              <p className="text-xl text-gray-300 max-w-2xl mx-auto tracking-wide">
                Hear what teachers and institutions are saying about EduTutor.
              </p>
            </motion.div>
            
            <div className="grid md:grid-cols-3 gap-8 relative z-10">
              {[
                {
                  quote: "EduTutor has transformed how I teach complex physics concepts. Students are more engaged than ever.",
                  author: "Dr. Emily Chen",
                  role: "Physics Professor, MIT",
                  gradient: "from-blue-500/10 to-purple-500/10"
                },
                {
                  quote: "We've seen a 40% improvement in student comprehension after integrating EduTutor videos into our curriculum.",
                  author: "Michael Rodriguez",
                  role: "Principal, Lincoln High School",
                  gradient: "from-cyan-500/10 to-blue-500/10"
                },
                {
                  quote: "The ability to create custom educational content in seconds has revolutionized our online learning platform.",
                  author: "Sarah Johnson",
                  role: "Director of E-Learning, Coursera",
                  gradient: "from-purple-500/10 to-pink-500/10"
                }
              ].map((testimonial, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 30 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: index * 0.2, duration: 0.7 }}
                  className="group relative"
                >
                  <div className={`absolute inset-0 bg-gradient-to-br ${testimonial.gradient} rounded-3xl blur-xl opacity-30 -z-10 group-hover:opacity-50 transition-opacity duration-500`} />
                  <div className="relative bg-gradient-to-br from-gray-900/50 to-black/50 rounded-3xl p-8 border border-gray-800 backdrop-blur-sm h-full hover:border-gray-700 transition-all duration-300">
                    <div className="text-3xl text-blue-400 mb-4">"</div>
                    <p className="text-gray-300 mb-8 leading-relaxed">{testimonial.quote}</p>
                    <div className="flex items-center gap-4">
                      <div className="size-10 rounded-xl bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center overflow-hidden">
                        <img src="/images/v4.png" alt="EduTutor Logo" className="w-full h-full object-contain rounded-lg" />
                      </div>
                      <div>
                        <h4 className="font-semibold text-white">{testimonial.author}</h4>
                        <p className="text-gray-400 text-sm">{testimonial.role}</p>
                      </div>
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>
          </section>

          {/* CTA Section */}
          <section className="container mx-auto px-6 py-28">
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true, margin: "-100px" }}
              transition={{ duration: 0.8 }}
              className="relative bg-gradient-to-br from-blue-600/20 to-purple-600/20 rounded-3xl p-12 md:p-24 text-center border border-blue-500/20 backdrop-blur-sm overflow-hidden"
            >
              <div className="absolute inset-0 bg-gradient-to-br from-blue-500/10 to-purple-500/10 rounded-3xl blur-xl -z-10" />
              
              {/* Enhanced decorative elements */}
              <div className="absolute top-0 right-0 size-96 bg-blue-600/15 rounded-full blur-3xl -z-10" />
              <div className="absolute bottom-0 left-0 size-96 bg-purple-600/15 rounded-full blur-3xl -z-10" />
              
              {/* Grid background */}
              <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.02)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.02)_1px,transparent_1px)] bg-[size:20px_20px]" />
              
              <h2 className="font-bold text-4xl md:text-6xl text-white mb-8 relative [text-shadow:0_0_25px_rgba(79,70,229,0.2)]">
                <span className="absolute -inset-1 bg-gradient-to-tr from-purple-500/5 to-blue-500/5 rounded-3xl blur-3xl -z-10"></span>
                Ready for Personalized Learning?
              </h2>
              <p className="text-xl text-gray-300 mb-12 max-w-2xl mx-auto relative tracking-wide">
                Join thousands of students who are mastering subjects faster with personalized AI video tutorials.
              </p>
              <Button className="bg-blue-600 hover:bg-blue-500 text-white rounded-2xl h-16 px-12 text-lg font-semibold shadow-2xl shadow-blue-600/25 border border-blue-500/20 transition-all duration-300 hover:shadow-xl hover:shadow-blue-600/30 group relative">
                Start Learning Now
                <ArrowRight className="ml-3 h-5 w-5 group-hover:translate-x-1 transition-transform" />
              </Button>
            </motion.div>
          </section>
        </>
      </main>

      <footer className="relative z-10 container mx-auto px-6 py-16 border-t border-gray-800">
        <div className="grid md:grid-cols-4 gap-12">
          <div className="md:col-span-1">
            <div className="flex items-center gap-3 mb-6">
              <div className="size-10 rounded-xl bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center overflow-hidden">
                <img src="/images/v4.png" alt="EduTutor Logo" className="w-full h-full object-contain rounded-lg" />
              </div>
              <span className="font-bold text-xl text-white">EduTutor</span>
            </div>
            <p className="text-gray-400 mb-6">Transforming education with AI-powered video generation and animation.</p>
            <div className="flex items-center gap-4">
              <Link href="https://github.com" className="text-gray-400 hover:text-white transition-colors">
                <Github className="h-5 w-5" />
              </Link>
            </div>
          </div>
          
          <div className="md:col-span-3 grid grid-cols-2 md:grid-cols-3 gap-8">
            <div>
              <h4 className="text-white font-semibold mb-4">Product</h4>
              <ul className="space-y-3">
                <li><Link href="#" className="text-gray-400 hover:text-white transition-colors">Features</Link></li>
                <li><Link href="#" className="text-gray-400 hover:text-white transition-colors">Pricing</Link></li>
                <li><Link href="#" className="text-gray-400 hover:text-white transition-colors">Roadmap</Link></li>
              </ul>
            </div>
            <div>
              <h4 className="text-white font-semibold mb-4">Company</h4>
              <ul className="space-y-3">
                <li><Link href="#" className="text-gray-400 hover:text-white transition-colors">About Us</Link></li>
                <li><Link href="#" className="text-gray-400 hover:text-white transition-colors">Careers</Link></li>
                <li><Link href="#" className="text-gray-400 hover:text-white transition-colors">Blog</Link></li>
              </ul>
            </div>
            <div>
              <h4 className="text-white font-semibold mb-4">Resources</h4>
              <ul className="space-y-3">
                <li><Link href="#" className="text-gray-400 hover:text-white transition-colors">Documentation</Link></li>
                <li><Link href="#" className="text-gray-400 hover:text-white transition-colors">Help Center</Link></li>
                <li><Link href="#" className="text-gray-400 hover:text-white transition-colors">Contact</Link></li>
              </ul>
            </div>
          </div>
        </div>
        
        <div className="mt-16 pt-8 border-t border-gray-800 flex flex-col md:flex-row justify-between items-center">
          <p className="text-gray-400 text-sm mb-4 md:mb-0">© 2025 EduTutor. All rights reserved.</p>
          <div className="flex items-center gap-8">
            <Link href="#" className="text-gray-400 hover:text-white text-sm transition-colors">Privacy Policy</Link>
            <Link href="#" className="text-gray-400 hover:text-white text-sm transition-colors">Terms of Service</Link>
          </div>
        </div>
      </footer>
    </div>
  )
}
