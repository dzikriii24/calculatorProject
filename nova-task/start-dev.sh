#!/bin/bash

echo "🚀 Starting Nova Task Development Environment"
echo "=============================================="

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+ first."
    exit 1
fi

# Check Node.js version
NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    echo "❌ Node.js version 18+ is required. Current version: $(node -v)"
    exit 1
fi

echo "✅ Node.js version: $(node -v)"

# Check if dependencies are installed
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

# Check if backend server is running
echo "🔍 Checking backend server connection..."
if curl -s http://127.0.0.1:8080 > /dev/null 2>&1; then
    echo "✅ Backend server is running on http://127.0.0.1:8080"
else
    echo "⚠️  Backend server is not running on http://127.0.0.1:8080"
    echo "   Please start the Go backend server first:"
    echo "   git clone https://github.com/u289-bit/trialtask"
    echo "   cd trialtask"
    echo "   # Follow the README to start the server"
    echo ""
fi

echo ""
echo "🌐 Starting frontend development server..."
echo "   The application will be available at: http://localhost:3000"
echo "   Press Ctrl+C to stop the server"
echo ""

# Start the development server
npm run dev