"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Loader2, Play, Sparkles, Brain, Zap } from "lucide-react"
import { motion, AnimatePresence } from "framer-motion"
import { useRouter } from "next/navigation"

type VideoGeneratorProps = {}

export default function VideoGenerator() {
  const [topic, setTopic] = useState("")
  const [isGenerating, setIsGenerating] = useState(false)
  const [generationStep, setGenerationStep] = useState(0)
  const router = useRouter()

  const generationSteps = [
    { icon: Brain, title: "Analyzing Topic", description: "Understanding the educational concept" },
    { icon: Sparkles, title: "Creating Animations", description: "Generating custom p5.js visualizations" },
    { icon: Zap, title: "Synthesizing Voice", description: "Creating natural AI narration" },
    { icon: Play, title: "Finalizing Video", description: "Combining all elements together" },
  ]

  const handleGenerate = () => {
    if (!topic) return

    setIsGenerating(true)
    setGenerationStep(0)

    // Simulate generation process with step progression
    const stepInterval = setInterval(() => {
      setGenerationStep((prev) => {
        if (prev >= 3) {
          clearInterval(stepInterval)
          setTimeout(() => {
            // Navigate to video player page
            router.push(`/video?topic=${encodeURIComponent(topic)}`)
          }, 1000)
          return prev
        }
        return prev + 1
      })
    }, 2000)
  }

  return (
    <div className="min-h-screen bg-black relative overflow-hidden">
      {/* Background effects */}
      <div className="absolute inset-0 bg-[linear-gradient(rgba(79,70,229,0.03)_1px,transparent_1px),linear-gradient(90deg,rgba(79,70,229,0.03)_1px,transparent_1px)] bg-[size:50px_50px] [mask-image:radial-gradient(ellipse_80%_50%_at_50%_0%,#000_70%,transparent_110%)]" />

      <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl animate-pulse" />
      <div className="absolute bottom-1/4 right-1/4 w-80 h-80 bg-purple-500/10 rounded-full blur-3xl animate-pulse delay-1000" />

      <div className="relative z-10 container mx-auto px-6 py-12">
        <div className="max-w-4xl mx-auto">
          <AnimatePresence mode="wait">
            {!isGenerating ? (
              <motion.div
                key="input"
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -30 }}
                className="text-center"
              >
                <h1 className="font-bold text-4xl md:text-6xl text-white mb-6 leading-tight">
                  What would you like to{" "}
                  <span className="bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
                    learn today?
                  </span>
                </h1>
                <p className="text-xl text-gray-300 mb-12 max-w-2xl mx-auto">
                  Enter any educational topic and watch as AI transforms it into an engaging visual learning experience.
                </p>

                <div className="max-w-2xl mx-auto space-y-6">
                  <div className="relative">
                    <Input
                      placeholder="e.g. Pythagorean Theorem, Photosynthesis, French Revolution..."
                      className="h-16 text-lg rounded-2xl border-gray-700 bg-gray-900/50 text-white placeholder-gray-400 focus:border-blue-500 focus:ring-blue-500 backdrop-blur-sm"
                      value={topic}
                      onChange={(e) => setTopic(e.target.value)}
                      onKeyPress={(e) => e.key === "Enter" && handleGenerate()}
                    />
                    <div className="absolute inset-0 rounded-2xl bg-gradient-to-r from-blue-500/20 to-purple-500/20 blur-xl -z-10 opacity-50" />
                  </div>

                  <Button
                    onClick={handleGenerate}
                    disabled={!topic}
                    className={`h-16 text-lg rounded-2xl px-12 font-semibold shadow-2xl border transition-all duration-300 ${
                      !topic
                        ? "bg-gray-800 text-gray-400 border-gray-700"
                        : "bg-blue-600 hover:bg-blue-700 text-white border-blue-500/20 shadow-blue-600/25 hover:shadow-blue-600/40"
                    }`}
                  >
                    <Sparkles className="mr-3 h-5 w-5" />
                    Generate Educational Video
                  </Button>
                </div>

                <div className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-6 max-w-3xl mx-auto">
                  {["Quantum Physics Basics", "Climate Change Effects", "Ancient Roman Empire"].map(
                    (example, index) => (
                      <motion.button
                        key={index}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.2 + index * 0.1 }}
                        onClick={() => setTopic(example)}
                        className="p-4 rounded-xl border border-gray-700 bg-gray-900/30 hover:bg-gray-800/50 text-gray-300 hover:text-white transition-all backdrop-blur-sm"
                      >
                        {example}
                      </motion.button>
                    ),
                  )}
                </div>
              </motion.div>
            ) : (
              <motion.div
                key="generating"
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                className="text-center"
              >
                <h2 className="font-bold text-3xl md:text-4xl text-white mb-4">Creating Your Educational Video</h2>
                <p className="text-xl text-gray-300 mb-12">
                  Topic: <span className="text-blue-400">{topic}</span>
                </p>

                <div className="max-w-3xl mx-auto">
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
                          className={`relative p-6 rounded-2xl border backdrop-blur-sm transition-all duration-500 ${
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
                    className="bg-gradient-to-br from-gray-900/50 to-black/50 rounded-2xl p-8 border border-gray-800 backdrop-blur-sm"
                  >
                    <div className="flex items-center justify-center gap-3 mb-4">
                      <Loader2 className="h-6 w-6 text-blue-400 animate-spin" />
                      <span className="text-white font-medium">Processing...</span>
                    </div>
                    <div className="w-full bg-gray-700 rounded-full h-2">
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
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
    </div>
  )
}
