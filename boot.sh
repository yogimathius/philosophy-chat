#!/bin/bash

# Boot script for Philosophy Chat (React + Vite)
set -e

echo "💭 Booting Philosophy Chat..."

# Check if pnpm is installed
if ! command -v pnpm &> /dev/null; then
    echo "❌ pnpm is not installed. Please install it first:"
    echo "npm install -g pnpm"
    exit 1
fi

# Check for .env file
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found. Creating template..."
    echo "VITE_OPENAI_API_KEY=your_api_key_here" > .env
    echo "📝 Please edit .env file and add your OpenAI API key"
fi

# Install dependencies
echo "📦 Installing dependencies..."
pnpm install

# Start development server
echo "🚀 Starting development server..."
echo "   Available at: http://localhost:5173"
echo "   Note: Make sure you've set your OpenAI API key in .env"
pnpm dev