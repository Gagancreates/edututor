'use client';

import { useEffect, useRef, useState } from 'react';
import Script from 'next/script';
import ErrorBoundary from './ErrorBoundary';

// Add p5 to Window interface
declare global {
  interface Window {
    p5: any;
  }
}

interface P5RendererProps {
  code: string;
  isPlaying: boolean;
}

// The actual P5.js renderer component
const P5Canvas = ({ code, isPlaying }: P5RendererProps) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const [p5Loaded, setP5Loaded] = useState(false);
  const [loadAttempts, setLoadAttempts] = useState(0);
  const [p5Instance, setP5Instance] = useState<any>(null);
  
  // Handle p5.js library loading
  const handleP5Load = () => {
    console.log('P5.js onLoad callback triggered');
    setP5Loaded(true);
  };
  
  // Check if p5 is loaded
  useEffect(() => {
    if (p5Loaded || !code || loadAttempts >= 10) return;
    
    const checkP5Loaded = () => {
      if (typeof window !== 'undefined' && window.p5) {
        console.log('P5.js detected in window object');
        setP5Loaded(true);
        return true;
      }
      return false;
    };
    
    if (checkP5Loaded()) return;
    
    const intervalId = setInterval(() => {
      if (checkP5Loaded()) {
        clearInterval(intervalId);
      } else {
        setLoadAttempts(prev => prev + 1);
        if (loadAttempts >= 10) {
          console.error('Failed to detect P5.js after multiple attempts');
          clearInterval(intervalId);
        }
      }
    }, 500);
    
    return () => clearInterval(intervalId);
  }, [code, p5Loaded, loadAttempts]);
  
  // Manually load P5.js if needed
  useEffect(() => {
    if (p5Loaded || !code || typeof window === 'undefined') return;
    
    if (loadAttempts >= 5 && !window.p5) {
      const script = document.createElement('script');
      script.src = 'https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.6.0/p5.min.js';
      script.onload = () => setP5Loaded(true);
      document.head.appendChild(script);
    }
  }, [code, p5Loaded, loadAttempts]);
  
  // Initialize P5.js sketch
  useEffect(() => {
    if (!code || !containerRef.current || !p5Loaded) return;
    
    console.log('Creating P5.js sketch...');
    
    // Clean up any existing instances
    if (p5Instance) {
      console.log('Removing previous P5.js instance');
      p5Instance.remove();
      setP5Instance(null);
    }
    
    const container = containerRef.current;
    
    // Clear any existing content
    container.innerHTML = '';
    
    try {
      // Create a centered container for the canvas
      const centeringDiv = document.createElement('div');
      centeringDiv.style.display = 'flex';
      centeringDiv.style.justifyContent = 'center';
      centeringDiv.style.alignItems = 'center';
      centeringDiv.style.width = '100%';
      centeringDiv.style.height = '100%';
      container.appendChild(centeringDiv);
      
      // Create the sketch function
      const sketch = (p: any) => {
        // Store the original setup and draw functions
        let originalSetup = p.setup;
        
        // Default setup if none provided
        if (!originalSetup) {
          originalSetup = function() {
            p.createCanvas(500, 300);
            p.background(0);
          };
        }
        
        // Override setup
        p.setup = function() {
          // Call the original setup to create the canvas
          originalSetup.call(p);
          
          // Get the created canvas and ensure it's centered
          const canvas = document.querySelector('canvas');
          if (canvas && canvas.parentNode) {
            // Move canvas to our centering div
            centeringDiv.appendChild(canvas);
          }
        };
        
        // Execute the user's code in this context
        try {
          new Function('p', code)(p);
        } catch (error) {
          console.error('Error executing user code:', error);
        }
      };
      
      // Create a new P5 instance
      if (window.p5) {
        const instance = new window.p5(sketch);
        setP5Instance(instance);
        console.log('P5.js sketch created successfully');
      }
    } catch (error) {
      console.error('Error creating P5.js sketch:', error);
      
      const errorMessage = document.createElement('div');
      errorMessage.className = 'text-red-500 text-center p-4 bg-gray-800 rounded';
      errorMessage.textContent = `Error: ${error instanceof Error ? error.message : 'Unknown error'}`;
      container.appendChild(errorMessage);
    }
    
    return () => {
      // Clean up on unmount
      if (p5Instance) {
        p5Instance.remove();
      }
    };
  }, [code, p5Loaded, p5Instance]);
  
  return (
    <div className="w-full bg-gray-900 rounded-lg overflow-hidden flex justify-center items-center">
      <Script 
        src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.6.0/p5.min.js" 
        strategy="beforeInteractive"
        onLoad={handleP5Load}
      />
      
      <div 
        ref={containerRef}
        className="w-full flex items-center justify-center"
        style={{ 
          minHeight: '400px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center'
        }}
      >
        {!code && (
          <div className="text-white text-center">
            <p>Enter a topic to generate a visualization</p>
          </div>
        )}
        
        {code && !p5Loaded && (
          <div className="text-white text-center">
            <div className="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-purple-600 mb-2"></div>
            <p>Loading P5.js library...</p>
          </div>
        )}
      </div>
    </div>
  );
};

// Wrapper component with error boundary
const P5Renderer = (props: P5RendererProps) => {
  return (
    <ErrorBoundary
      fallback={
        <div className="w-full h-96 flex items-center justify-center bg-gray-900 relative">
          <div className="bg-red-500/20 border border-red-500/30 rounded-lg p-4 text-white max-w-md">
            <h2 className="text-lg font-bold mb-2">Error Rendering Visualization</h2>
            <p className="text-sm opacity-80 mb-4">
              The P5.js visualization failed to render. Please try a different topic or refresh the page.
            </p>
          </div>
        </div>
      }
    >
      <P5Canvas {...props} />
    </ErrorBoundary>
  );
};

export default P5Renderer; 