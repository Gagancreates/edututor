"use client"

import { motion, AnimatePresence } from "framer-motion"
import { Button } from "@/components/ui/button"
import { Github } from "lucide-react"
import Link from "next/link"

interface MobileMenuProps {
  isOpen: boolean;
}

export default function MobileMenu({ isOpen }: MobileMenuProps) {
  return (
    <AnimatePresence>
      {isOpen && (
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
  )
} 