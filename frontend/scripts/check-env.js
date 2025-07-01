#!/usr/bin/env node

/**
 * Script to check if environment variables are set up correctly
 * Run this with npm run check-env
 */

require('dotenv').config({ path: '.env.local' });

// Get environment variables
const GEMINI_API_KEY = process.env.GEMINI_API_KEY;
const ELEVEN_LABS_API_KEY = process.env.ELEVEN_LABS_API_KEY;

// Check if required environment variables are set
const missingVars = [];
if (!GEMINI_API_KEY) missingVars.push('GEMINI_API_KEY');
if (!ELEVEN_LABS_API_KEY) missingVars.push('ELEVEN_LABS_API_KEY');

if (missingVars.length > 0) {
  console.error('\x1b[31m%s\x1b[0m', '❌ Error: Missing required environment variables:');
  missingVars.forEach(variable => {
    console.error(`   - ${variable}`);
  });
  console.error('\n\x1b[33m%s\x1b[0m', 'Please create or update your .env.local file with these variables.');
  console.error('\x1b[36m%s\x1b[0m', 'Example .env.local file:');
  console.error(`GEMINI_API_KEY=your_gemini_api_key_here
ELEVEN_LABS_API_KEY=your_elevenlabs_api_key_here`);

  process.exit(1);
} else {
  console.log('\x1b[32m%s\x1b[0m', '✅ Environment variables are correctly set up!');
  console.log('\x1b[36m%s\x1b[0m', '   - GEMINI_API_KEY: ' + '✓');
  console.log('\x1b[36m%s\x1b[0m', '   - ELEVEN_LABS_API_KEY: ' + '✓');
  
  process.exit(0);
} 