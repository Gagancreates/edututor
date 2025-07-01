'use client';

import { useState, useEffect } from 'react';
import P5Renderer from '@/components/P5Renderer';
import AudioPlayer from '@/components/AudioPlayer';
import Link from 'next/link';

export default function LearnPage() {
  const [topic, setTopic] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [p5jsCode, setP5jsCode] = useState('');
  const [script, setScript] = useState<any>(null);
  const [audioUrl, setAudioUrl] = useState<string | undefined>(undefined);
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentSection, setCurrentSection] = useState('intro');
  const [needsApiKeys, setNeedsApiKeys] = useState(false);

  // Test P5.js example
  const loadTestExample = () => {
    const testCode = `
    p.setup = function() {
      p.createCanvas(600, 350);
      p.background(0);
      
      // Draw a border to check alignment
      p.stroke(255, 0, 0);
      p.strokeWeight(4);
      p.noFill();
      p.rect(2, 2, p.width-4, p.height-4);
      
      p.noStroke();
      p.fill(255);
      p.textSize(24);
      p.textAlign(p.CENTER, p.CENTER);
      p.text("P5.js is working! Move your mouse around.", p.width/2, p.height/2);
      
      // Draw alignment markers
      p.fill(0, 255, 0);
      p.rect(p.width/2 - 5, 0, 10, 10); // Top center
      p.rect(p.width - 10, p.height/2 - 5, 10, 10); // Right center
      p.rect(p.width/2 - 5, p.height - 10, 10, 10); // Bottom center
      p.rect(0, p.height/2 - 5, 10, 10); // Left center
    };
    
    p.draw = function() {
      // Slowly fade background but preserve the border and markers
      p.fill(0, 15);
      p.rect(10, 10, p.width-20, p.height-20);
      
      // Calculate colors based on mouse position
      let r = p.map(p.mouseX, 0, p.width, 50, 255);
      let g = p.map(p.mouseY, 0, p.height, 50, 255);
      let b = p.map(p.mouseX + p.mouseY, 0, p.width + p.height, 50, 255);
      
      // Draw a circle where the mouse is
      p.fill(r, g, b, 200);
      let size = p.sin(p.frameCount * 0.05) * 10 + 30;
      p.ellipse(p.mouseX, p.mouseY, size, size);
      
      // Draw some text at the top
      p.fill(255);
      p.textSize(14);
      p.text("Canvas should be centered with red border visible", p.width/2, 30);
    };
    `;
    
    setP5jsCode(testCode);
    setScript({
      intro: "This is a test visualization showing that P5.js is working correctly. The colorful circle follows your mouse movement.",
      frames: [{
        time: "0-5s",
        narration: "Move your mouse around to see the interactive elements. The circle changes color based on your mouse position."
      }],
      conclusion: "If you can see the animation centered in the display area, P5.js is working correctly."
    });
    
    // Generate test audio
    generateAudio("This is a test visualization showing that P5.js is working correctly. The colorful circle follows your mouse movement.");
    setCurrentSection('intro');
  };

  // Check if API keys are configured
  useEffect(() => {
    const checkApiKeys = async () => {
      try {
        // Check Gemini API
        const geminiRes = await fetch('/api/generate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ topic: 'test' }),
        });
        
        // Check ElevenLabs API
        const elevenLabsRes = await fetch('/api/text-to-speech', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ text: 'test' }),
        });
        
        // If either API check fails, show the API keys required message
        const geminiData = await geminiRes.json();
        const elevenLabsData = await elevenLabsRes.json();
        
        if (!geminiRes.ok || !elevenLabsRes.ok || 
            (geminiData.error && geminiData.error.includes('API key')) || 
            (elevenLabsData.error && elevenLabsData.error.includes('API key'))) {
          setNeedsApiKeys(true);
        } else {
          setNeedsApiKeys(false);
        }
      } catch (err) {
        console.error('Error checking APIs:', err);
        // Don't automatically assume API keys are missing on any error
      }
    };
    
    checkApiKeys();
  }, []);

  const handleGenerateContent = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!topic.trim()) {
      setError('Please enter a topic');
      return;
    }
    
    setLoading(true);
    setError(null);
    setP5jsCode('');
    setScript(null);
    setAudioUrl(undefined);
    
    try {
      // Step 1: Generate P5.js code and script
      const generateResponse = await fetch('/api/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ topic }),
      });
      
      if (!generateResponse.ok) {
        throw new Error('Failed to generate content');
      }
      
      const generateData = await generateResponse.json();
      console.log('P5.js code received:', generateData.p5jsCode?.substring(0, 100) + '...');
      setP5jsCode(generateData.p5jsCode);
      setScript(generateData.script);
      
      // Step 2: Convert intro text to speech
      await generateAudio(generateData.script.intro);
      setCurrentSection('intro');
      
    } catch (err) {
      console.error('Error generating content:', err);
      setError('Failed to generate content. Please try again.');
    } finally {
      setLoading(false);
    }
  };
  
  const generateAudio = async (text: string) => {
    try {
      const ttsResponse = await fetch('/api/text-to-speech', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text }),
      });
      
      if (!ttsResponse.ok) {
        throw new Error('Failed to convert text to speech');
      }
      
      const ttsData = await ttsResponse.json();
      setAudioUrl(ttsData.audioUrl);
      setIsPlaying(true);
      
    } catch (err) {
      console.error('Error generating audio:', err);
      setError('Failed to generate audio. Please try again.');
    }
  };
  
  const handleAudioEnded = () => {
    if (!script) return;
    
    // Progress to the next section of the script
    if (currentSection === 'intro' && script.frames && script.frames.length > 0) {
      setCurrentSection('frame0');
      generateAudio(script.frames[0].narration);
    } else if (currentSection.startsWith('frame')) {
      const currentFrameIndex = parseInt(currentSection.replace('frame', ''));
      const nextFrameIndex = currentFrameIndex + 1;
      
      if (script.frames && nextFrameIndex < script.frames.length) {
        setCurrentSection(`frame${nextFrameIndex}`);
        generateAudio(script.frames[nextFrameIndex].narration);
      } else {
        setCurrentSection('conclusion');
        generateAudio(script.conclusion);
      }
    }
  };
  
  return (
    <div className="min-h-screen bg-gray-950 text-white py-12">
      <div className="container mx-auto px-4">
        <h1 className="text-4xl font-bold mb-8 text-center">
          Your Personal AI Video Tutor
        </h1>
        
        {needsApiKeys ? (
          <div className="max-w-3xl mx-auto bg-red-500/20 border border-red-500/30 rounded-lg p-6 mb-8">
            <h2 className="text-xl font-bold mb-2">API Keys Required</h2>
            <p className="mb-4">
              To use this demo, you need to configure your Gemini and ElevenLabs API keys.
              Create a .env.local file in the root of the project with the following:
            </p>
            <pre className="bg-black/50 p-4 rounded-md mb-4 overflow-x-auto">
              GEMINI_API_KEY=your_gemini_api_key_here<br/>
              ELEVEN_LABS_API_KEY=your_elevenlabs_api_key_here
            </pre>
            <p className="text-sm">
              <a href="https://ai.google.dev/" className="text-blue-400 hover:underline" target="_blank" rel="noopener noreferrer">Get a Gemini API key</a>
              {' '} | {' '}
              <a href="https://elevenlabs.io/" className="text-blue-400 hover:underline" target="_blank" rel="noopener noreferrer">Get an ElevenLabs API key</a>
            </p>
            <div className="mt-4">
              <Link href="/" className="inline-block px-4 py-2 bg-blue-600 hover:bg-blue-500 rounded-lg transition-colors">
                Return to Home
              </Link>
            </div>
          </div>
        ) : (
          <div className="max-w-3xl mx-auto">
            <form onSubmit={handleGenerateContent} className="mb-8">
              <div className="flex gap-4">
                <input
                  type="text"
                  value={topic}
                  onChange={(e) => setTopic(e.target.value)}
                  placeholder="Enter a topic to learn (e.g., 'How gravity works')"
                  className="flex-1 p-3 rounded-lg bg-gray-800 border border-gray-700 focus:outline-none focus:ring-2 focus:ring-purple-600"
                />
                <button
                  type="submit"
                  disabled={loading}
                  className="px-6 py-3 bg-purple-600 rounded-lg font-medium hover:bg-purple-700 transition-colors disabled:opacity-50"
                >
                  {loading ? 'Generating...' : 'Generate Tutorial'}
                </button>
              </div>
              <div className="mt-2 flex justify-end">
                <button
                  type="button"
                  onClick={loadTestExample}
                  className="text-sm bg-gray-700 px-3 py-1 rounded hover:bg-gray-600 transition-colors"
                >
                  🧪 Test P5.js Renderer
                </button>
              </div>
              {error && (
                <p className="mt-2 text-red-500">{error}</p>
              )}
            </form>
            
            {loading && (
              <div className="text-center py-16">
                <div className="inline-block animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-purple-600 mb-4"></div>
                <p className="text-lg">Generating your educational content...</p>
                <p className="text-sm text-gray-400 mt-2">This may take up to a minute</p>
              </div>
            )}
            
            {p5jsCode && (
              <div className="space-y-6">
                {/* <div className="flex justify-center items-center">
                  <P5Renderer code={p5jsCode} isPlaying={isPlaying} />
                </div> */}
                
                <AudioPlayer
                  p5jsCode={p5jsCode}
                  audioUrl={audioUrl}
                  isPlaying={isPlaying}
                  onPlayPause={setIsPlaying}
                  onEnded={handleAudioEnded}
                />
                
                {script && (
                  <div className="bg-gray-800 rounded-lg p-4">
                    <h2 className="text-xl font-semibold mb-2">Current Section: {currentSection}</h2>
                    <div className="prose prose-invert max-w-none">
                      {currentSection === 'intro' && <p>{script.intro}</p>}
                      {currentSection.startsWith('frame') && script.frames && (
                        <p>{script.frames[parseInt(currentSection.replace('frame', ''))].narration}</p>
                      )}
                      {currentSection === 'conclusion' && <p>{script.conclusion}</p>}
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
} 