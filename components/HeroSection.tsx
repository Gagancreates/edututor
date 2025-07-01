"use client"

import { motion, AnimatePresence } from "framer-motion"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { ArrowRight, Play, Sparkles, Brain, Zap, Loader2 } from "lucide-react"
import Link from "next/link"

interface HeroSectionProps {
  searchTopic: string;
  setSearchTopic: (topic: string) => void;
  isGenerating: boolean;
  setIsGenerating: (generating: boolean) => void;
  generationStep: number;
  generationSteps: {
    icon: string;
    title: string;
    description: string;
  }[];
  handleGenerate: () => void;
  isMobile: boolean;
}

export default function HeroSection({
  searchTopic,
  setSearchTopic,
  isGenerating,
  setIsGenerating,
  generationStep,
  generationSteps,
  handleGenerate,
  isMobile
}: HeroSectionProps) {
  
  // Map string icon names to actual components
  const iconComponents = {
    Brain,
    Sparkles,
    Zap,
    Play
  };
  
  return (
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
                      const isActive = index === generationStep;
                      const isCompleted = index < generationStep;
                      const IconComponent = iconComponents[step.icon as keyof typeof iconComponents];

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
                      );
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
    </section>
  );
} 