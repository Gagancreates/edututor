/**
 * Environment variable validation helper
 */

// Get environment variables with validation
export const getEnv = () => {
  const GEMINI_API_KEY = process.env.GEMINI_API_KEY;
  const ELEVEN_LABS_API_KEY = process.env.ELEVEN_LABS_API_KEY;

  // Check if required environment variables are set
  const missingVars = [];
  if (!GEMINI_API_KEY) missingVars.push('GEMINI_API_KEY');
  if (!ELEVEN_LABS_API_KEY) missingVars.push('ELEVEN_LABS_API_KEY');

  return {
    GEMINI_API_KEY,
    ELEVEN_LABS_API_KEY,
    isConfigured: missingVars.length === 0,
    missingVars
  };
}; 