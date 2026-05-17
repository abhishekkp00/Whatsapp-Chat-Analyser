#!/bin/bash

# WhatsApp Chat Analyzer - Quick Start Guide
# This script will set up and run your application

set -e

echo "╔════════════════════════════════════════════════════════════╗"
echo "║      WhatsApp Chat Analyzer - Quick Start Setup            ║"
echo "║                  All Errors Fixed! ✅                      ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Check Python version
echo "🐍 Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed!"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "✅ Python $PYTHON_VERSION found"
echo ""

# Install dependencies
echo "📦 Installing dependencies from requirements.txt..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║              Setup Complete! Ready to Run                  ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "📊 To start the application, run:"
echo "   streamlit run app.py"
echo ""
echo "📤 Steps to analyze your WhatsApp chat:"
echo "   1. Open WhatsApp on your phone"
echo "   2. Select the chat you want to analyze"
echo "   3. Tap Menu (⋮) → More → Export chat"
echo "   4. Choose 'Without media' for faster analysis"
echo "   5. Save the .txt file"
echo "   6. Upload it to the web app"
echo "   7. View your detailed analysis!"
echo ""
echo "🎉 Happy analyzing!"
echo ""
