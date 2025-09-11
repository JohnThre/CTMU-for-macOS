#!/bin/bash
# CTMU Swiss Army Knife Installation Script

echo "🛠️  Installing CTMU Swiss Army Knife CLI Tool"
echo "=============================================="

# Check Python version
python_version=$(python3 --version 2>&1 | grep -o '[0-9]\+\.[0-9]\+')
if [[ $(echo "$python_version >= 3.8" | bc -l) -eq 0 ]]; then
    echo "❌ Python 3.8+ required. Current: $python_version"
    exit 1
fi

echo "✅ Python version: $python_version"

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

# Install CTMU
echo "🔧 Installing CTMU..."
pip3 install -e .

# Test installation
echo "🧪 Testing installation..."
if command -v ctmu &> /dev/null; then
    echo "✅ CTMU installed successfully!"
    echo ""
    echo "🚀 Quick start:"
    echo "   ctmu --help"
    echo "   ctmu qr https://github.com"
    echo "   ctmu hash text 'hello world'"
    echo "   ctmu sys info"
    echo ""
    echo "📚 Run 'python example.py' for full demonstrations"
else
    echo "❌ Installation failed. Try manual installation:"
    echo "   pip3 install -e ."
fi