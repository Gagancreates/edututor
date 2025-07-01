'use client';

import { useEffect, useRef, useState } from 'react';
import P5Renderer from './P5Renderer';

interface AudioPlayerProps {
  audioUrl?: string;
  isPlaying: boolean;
  onPlayPause: (isPlaying: boolean) => void;
  onEnded: () => void;
  p5jsCode: string;
}

const AudioPlayer = ({ audioUrl, isPlaying, onPlayPause, onEnded, p5jsCode }: AudioPlayerProps) => {
  const audioRef = useRef<HTMLAudioElement>(null);
  const [progress, setProgress] = useState(0);
  const [duration, setDuration] = useState(0);
  const [currentTime, setCurrentTime] = useState(0);

  useEffect(() => {
    if (!audioRef.current) return;

    const audio = audioRef.current;

    if (isPlaying) {
      audio.play().catch(err => {
        console.error('Failed to play audio:', err);
        onPlayPause(false);
      });
    } else {
      audio.pause();
    }
  }, [isPlaying, onPlayPause]);

  useEffect(() => {
    if (!audioRef.current || !audioUrl) return;
    
    // Reset player state when audio source changes
    setProgress(0);
    setCurrentTime(0);
    
    if (isPlaying) {
      audioRef.current.play().catch(err => {
        console.error('Failed to play new audio:', err);
        onPlayPause(false);
      });
    }
  }, [audioUrl, isPlaying, onPlayPause]);

  const handleTimeUpdate = () => {
    if (!audioRef.current) return;
    
    const audio = audioRef.current;
    setCurrentTime(audio.currentTime);
    setProgress((audio.currentTime / audio.duration) * 100);
  };

  const handleLoadedMetadata = () => {
    if (!audioRef.current) return;
    setDuration(audioRef.current.duration);
  };

  const handleSeek = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!audioRef.current) return;
    
    const audio = audioRef.current;
    const seekTime = (parseInt(e.target.value) / 100) * audio.duration;
    audio.currentTime = seekTime;
    setCurrentTime(seekTime);
    setProgress(parseInt(e.target.value));
  };

  const formatTime = (time: number) => {
    const minutes = Math.floor(time / 60);
    const seconds = Math.floor(time % 60);
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
  };

  return (
    <div className="w-full bg-gray-800 rounded-lg p-4 text-white">
      <div className="flex flex-col justify-center items-center mb-4">
        <div className="w-full max-w-full flex justify-center">
          <P5Renderer code={p5jsCode} isPlaying={isPlaying} />
        </div>
      </div>
      
      {audioUrl ? (
        <>
          <audio
            ref={audioRef}
            src={audioUrl}
            onTimeUpdate={handleTimeUpdate}
            onLoadedMetadata={handleLoadedMetadata}
            onEnded={() => {
              onPlayPause(false);
              onEnded();
            }}
          />
          <div className="flex items-center space-x-4">
            <button
              onClick={() => onPlayPause(!isPlaying)}
              className="p-2 rounded-full bg-purple-600 hover:bg-purple-700 transition-colors"
            >
              {isPlaying ? (
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <rect x="6" y="4" width="4" height="16"></rect>
                  <rect x="14" y="4" width="4" height="16"></rect>
                </svg>
              ) : (
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <polygon points="5 3 19 12 5 21 5 3"></polygon>
                </svg>
              )}
            </button>
            <div className="flex-1">
              <input
                type="range"
                min="0"
                max="100"
                value={progress}
                onChange={handleSeek}
                className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer"
              />
              <div className="flex justify-between text-xs mt-1">
                <span>{formatTime(currentTime)}</span>
                <span>{formatTime(duration)}</span>
              </div>
            </div>
          </div>
        </>
      ) : (
        <div className="text-center py-4">
          <p>Generate audio narration to play</p>
        </div>
      )}
    </div>
  );
};

export default AudioPlayer; 