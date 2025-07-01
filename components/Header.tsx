"use client"

import { motion } from "framer-motion"
import { Button } from "@/components/ui/button"
import { Github, Menu, X } from "lucide-react"
import Link from "next/link"
import Image from "next/image"

interface HeaderProps {
  mobileMenuOpen: boolean;
  setMobileMenuOpen: (open: boolean) => void;
}

export default function Header({ mobileMenuOpen, setMobileMenuOpen }: HeaderProps) {
  return (
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
  )
} 