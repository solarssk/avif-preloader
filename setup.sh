#!/bin/bash

echo "🔧 Starting AVIF Preloader Setup..."

# 1. Check for Python 3
if ! command -v python3 &>/dev/null; then
    echo "❌ Python 3 is not installed. Please install it first."
    exit 1
else
    echo "✅ Python 3 is installed."
fi

# 2. Check for pip3
if ! command -v pip3 &>/dev/null; then
    echo "❌ pip3 is not installed. Attempting to install..."
    python3 -m ensurepip --upgrade || {
        echo "❌ Failed to install pip. Please install it manually."
        exit 1
    }
else
    echo "✅ pip3 is installed."
fi

# 3. Install required Python packages
echo "📦 Installing required packages..."
pip3 install --upgrade pip
pip3 install requests beautifulsoup4 "urllib3<2"

# 4. Run the Python script
echo "🚀 Running AVIF checker..."
python3 avif_preloader.py