#!/bin/bash

# Setup script for WhatsApp Chat Analyzer

echo "🚀 Setting up WhatsApp Chat Analyzer..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python 3 found"

# Create virtual environment (optional)
# echo "📦 Creating virtual environment..."
# python3 -m venv venv
# source venv/bin/activate

# Install requirements
echo "📚 Installing required packages..."
pip install -r requirements.txt

# Download TextBlob corpora
echo "📥 Downloading TextBlob corpora..."
python3 -m textblob.download_corpora 2>/dev/null || true

echo "✅ Setup complete!"
echo ""
echo "🎯 To run the application, use:"
echo "   streamlit run app.py"
echo ""
echo "📤 To export WhatsApp chat:"
echo "   1. Open WhatsApp"
echo "   2. Go to the chat you want to analyze"
echo "   3. Click Menu → More → Export chat"
echo "   4. Choose 'Without media'"
echo "   5. Save the .txt file and upload it to the app"
