#!/bin/bash

echo "🏗️  Building Nova Task for Production"
echo "====================================="

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+ first."
    exit 1
fi

# Check if dependencies are installed
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

echo "🔨 Building application..."
npm run build

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Build completed successfully!"
    echo "📁 Production files are in the .next/ directory"
    echo ""
    echo "🚀 To start the production server:"
    echo "   npm run start"
    echo ""
    echo "🌐 The application will be available at: http://localhost:3000"
else
    echo "❌ Build failed. Please check the error messages above."
    exit 1
fi