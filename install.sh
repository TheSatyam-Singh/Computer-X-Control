#!/bin/bash
# Computer-X-Control Installation Script

echo "🚀 Installing Computer-X-Control Dependencies"
echo "=============================================="

# Check Python version
echo "📋 Checking Python version..."
python3 --version

# Create virtual environment (optional but recommended)
echo "🔧 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate 2>/dev/null || echo "⚠️  Virtual environment activation failed (continuing anyway)"

# Upgrade pip
echo "📦 Upgrading pip..."
python3 -m pip install --upgrade pip

# Install core dependencies
echo "📚 Installing core dependencies..."
pip install python-dotenv psutil

# Install GUI automation dependencies
echo "🖱️  Installing GUI automation dependencies..."
echo "   Note: These may require system dependencies on Linux"
pip install pyautogui pillow opencv-python

# Install LLM dependencies
echo "🧠 Installing LLM dependencies..."
pip install openai anthropic

# Install web automation dependencies (optional)
echo "🌐 Installing web automation dependencies..."
pip install selenium webdriver-manager

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "⚙️  Creating .env file from template..."
    cp .env.example .env
    echo "✏️  Please edit .env file and add your API keys!"
else
    echo "✅ .env file already exists"
fi

echo ""
echo "✅ Installation completed!"
echo ""
echo "🔧 Next steps:"
echo "1. Edit .env file and add your LLM API keys"
echo "2. Test installation: python test_basic.py"
echo "3. Run demo: python demo.py"
echo "4. Start interactive mode: python main.py"
echo ""
echo "📖 For more information, see README.md"