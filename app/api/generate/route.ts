import { GoogleGenerativeAI } from '@google/generative-ai';
import { NextRequest, NextResponse } from 'next/server';
import { getEnv } from '@/lib/env';

// Initialize the Gemini API
const env = getEnv();
const genAI = new GoogleGenerativeAI(env.GEMINI_API_KEY || '');
const model = genAI.getGenerativeModel({ model: 'gemini-2.0-flash' });

export async function POST(request: NextRequest) {
  try {
    const { topic } = await request.json();
    
    if (!topic) {
      return NextResponse.json(
        { error: 'Topic is required' },
        { status: 400 }
      );
    }

    // For API key check from the frontend
    if (topic === 'test') {
      // Check if API key is configured
      if (!env.GEMINI_API_KEY) {
        return NextResponse.json(
          { error: 'Gemini API key is not configured' },
          { status: 500 }
        );
      }
      
      // API key exists, return success
      return NextResponse.json({ success: true });
    }

    // Check if environment is properly configured
    if (!env.isConfigured) {
      return NextResponse.json(
        { error: `Missing required environment variables: ${env.missingVars.join(', ')}` },
        { status: 500 }
      );
    }

    // Generate P5.js visualization code and script
    const prompt = `
    I need educational content about "${topic}". Please provide:
    
    1. P5.js code for a visualization that teaches about "${topic}". 
    The code should be well-commented, educational, and visually engaging.
    It should demonstrate concepts related to ${topic} in a visual way.
    The visualization should be animated and interactive where appropriate.
    
    IMPORTANT: The P5.js code MUST be structured for instance mode, using this format:
    
    \`\`\`
    p.setup = function() {
      // Setup code here
      p.createCanvas(width, height);
      p.background(color);
    };
    
    p.draw = function() {
      // Animation code here
    };
    
    // Any other functions should also use 'p.' prefix for ALL p5.js functions and variables
    // For example: p.ellipse(), p.rect(), p.fill(), p.width, p.height, etc.
    p.myFunction = function() {
      // Function code
    };
    \`\`\`
    
    DO NOT use any custom functions that are not defined in your code.
    
    2. A script for narration that explains what's happening in the visualization.
    The script should be educational, clear, and synchronized with the visualization.
    It should be broken down into sections/frames that correspond to stages in the visualization.
    
    Format your response as a JSON object with these properties:
    {
      "p5jsCode": "// Your complete P5.js code here in instance mode (using p.setup, p.draw format)",
      "script": {
        "intro": "Introduction text",
        "frames": [
          {
            "time": "0-5s",
            "narration": "What to say for this frame"
          },
          // More frames
        ],
        "conclusion": "Concluding remarks"
      }
    }
    `;

    const result = await model.generateContent(prompt);
    const response = await result.response;
    const text = response.text();
    
    console.log('Raw response from Gemini:', text.substring(0, 500) + '...');
    
    // Parse the response to extract JSON
    const jsonMatch = text.match(/```json\n([\s\S]*?)\n```/) || 
                      text.match(/```\n([\s\S]*?)\n```/) ||
                      text.match(/{[\s\S]*}/);
    
    let parsedResponse;
    let p5jsCode = '';
    let script = null;
    
    if (jsonMatch && jsonMatch[1]) {
      try {
        parsedResponse = JSON.parse(jsonMatch[1]);
      } catch (e) {
        // Try to parse the whole text as JSON
        try {
          parsedResponse = JSON.parse(text);
        } catch (e) {
          // Try to extract p5jsCode and script from non-JSON response
          const p5jsCodeMatch = text.match(/```(?:javascript|js)?\n([\s\S]*?)\n```/) || 
                               text.match(/p5jsCode["\s:=]+([\s\S]*?)(?=script|$)/i);
          
          if (p5jsCodeMatch && p5jsCodeMatch[1]) {
            p5jsCode = p5jsCodeMatch[1].trim();
            
            // Attempt to extract script
            const scriptMatch = text.match(/script["\s:=]+([\s\S]*?)(?=$)/i);
            if (scriptMatch && scriptMatch[1]) {
              try {
                script = JSON.parse(scriptMatch[1].trim());
              } catch (err) {
                // Construct a basic script object
                script = {
                  intro: "Let's explore this topic visually.",
                  frames: [],
                  conclusion: "This visualization helps us understand the concept."
                };
              }
            }
            
            return NextResponse.json({
              p5jsCode,
              script
            });
          } else {
            return NextResponse.json(
              { error: 'Failed to parse response from AI', rawText: text.substring(0, 1000) },
              { status: 500 }
            );
          }
        }
      }
    } else {
      try {
        // Try to parse the whole text as JSON
        parsedResponse = JSON.parse(text);
      } catch (e) {
        // Extract p5jsCode from non-JSON response
        const p5jsCodeMatch = text.match(/```(?:javascript|js)?\n([\s\S]*?)\n```/) || 
                             text.match(/p\.setup[\s\S]*?p\.draw/);
        
        if (p5jsCodeMatch && p5jsCodeMatch[0]) {
          p5jsCode = p5jsCodeMatch[0];
          
          // Construct a basic script object
          script = {
            intro: "Let's explore this topic visually.",
            frames: [],
            conclusion: "This visualization helps us understand the concept."
          };
          
          return NextResponse.json({
            p5jsCode,
            script
          });
        }
        
        return NextResponse.json(
          { error: 'Failed to parse response from AI', rawText: text.substring(0, 1000) },
          { status: 500 }
        );
      }
    }

    // Ensure p5jsCode follows the instance mode format
    if (parsedResponse.p5jsCode) {
      // If code doesn't use p.setup format, convert it
      if (!parsedResponse.p5jsCode.includes('p.setup') && parsedResponse.p5jsCode.includes('function setup()')) {
        try {
          const setupMatch = parsedResponse.p5jsCode.match(/function setup\(\) {([\s\S]*?)}/);
          const drawMatch = parsedResponse.p5jsCode.match(/function draw\(\) {([\s\S]*?)}/);
          
          const setupCode = setupMatch ? setupMatch[1] : 'createCanvas(710, 400); background(0);';
          const drawCode = drawMatch ? drawMatch[1] : '';
          
          // Remove the original setup and draw functions
          let otherCode = parsedResponse.p5jsCode
            .replace(/function setup\(\) {[\s\S]*?}/, '')
            .replace(/function draw\(\) {[\s\S]*?}/, '');
          
          // Convert to instance mode
          parsedResponse.p5jsCode = `
p.setup = function() {
  ${setupCode.replace(/(\W)(createCanvas|background|stroke|fill|rect|ellipse|line|beginShape|endShape|vertex|text|textSize|textAlign)/g, '$1p.$2')}
};

p.draw = function() {
  ${drawCode.replace(/(\W)(background|stroke|fill|rect|ellipse|line|beginShape|endShape|vertex|text|textSize|textAlign)/g, '$1p.$2')}
};

// Other functions
${otherCode.replace(/function (\w+)\(([^)]*)\) {([\s\S]*?)}/g, 'p.$1 = function($2) {$3}')}
`;
        } catch (error) {
          console.error('Error converting p5js code to instance mode:', error);
          // If conversion fails, provide a simple example instead of failing
          parsedResponse.p5jsCode = `
p.setup = function() {
  p.createCanvas(600, 350);
  p.background(0);
  p.fill(255);
  p.textSize(24);
  p.textAlign(p.CENTER, p.CENTER);
  p.text("Sorry, couldn't create a visualization for this topic.", p.width/2, p.height/2);
  p.textSize(14);
  p.text("Please try again with a different topic.", p.width/2, p.height/2 + 40);
};

p.draw = function() {
  // Just display the message
};
`;
        }
      }
    }

    return NextResponse.json({
      p5jsCode: parsedResponse.p5jsCode,
      script: parsedResponse.script
    });
    
  } catch (error) {
    console.error('Error generating content:', error);
    return NextResponse.json(
      { error: 'Failed to generate content' },
      { status: 500 }
    );
  }
} 