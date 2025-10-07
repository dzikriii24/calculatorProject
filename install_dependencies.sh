#!/bin/bash

echo "🔧 Installing Social Media Tracker Dependencies"
echo "=============================================="

# Update package list
echo "📦 Updating package list..."
sudo apt-get update

# Install Python3 and pip
echo "🐍 Installing Python3 and pip..."
sudo apt-get install -y python3 python3-pip python3-venv

# Install Chrome browser
echo "🌐 Installing Chrome browser..."
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | sudo tee /etc/apt/sources.list.d/google-chrome.list
sudo apt-get update
sudo apt-get install -y google-chrome-stable

# Install additional system dependencies
echo "📚 Installing system dependencies..."
sudo apt-get install -y chromium-chromedriver
sudo apt-get install -y xvfb
sudo apt-get install -y libnss3-dev libatk-bridge2.0-dev libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 libxrandr2 libgbm1 libxss1 libasound2

# Create virtual environment
echo "🏗️ Creating virtual environment..."
python3 -m venv tracker_env
source tracker_env/bin/activate

# Install Python packages
echo "📦 Installing Python packages..."
pip install --upgrade pip
pip install -r requirements.txt

# Install additional packages for better compatibility
echo "🔧 Installing additional packages..."
pip install webdriver-manager
pip install fake-useragent
pip install python-dotenv

echo ""
echo "✅ Installation completed!"
echo ""
echo "🚀 To run the tracker:"
echo "1. Activate virtual environment: source tracker_env/bin/activate"
echo "2. Run the program: python run_tracker.py"
echo ""
echo "⚠️  Make sure to use responsibly and legally!"