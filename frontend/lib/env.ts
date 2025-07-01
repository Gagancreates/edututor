/**
 * Environment variable validation helper
 */

// Get environment variables with validation
export const getEnv = () => {
  const BACKEND_API_URL = process.env.BACKEND_API_URL || 'http://localhost:8000';

  // For this implementation, we don't have any required environment variables
  // since we're using a default for BACKEND_API_URL
  const missingVars: string[] = [];

  return {
    BACKEND_API_URL,
    isConfigured: true, // Always configured since we have defaults
    missingVars
  };
}; 