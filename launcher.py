#!/usr/bin/env python3
"""
Computer-X-Control Quick Launcher

A simple script to quickly test and launch Computer-X-Control
with various options.
"""

import sys
import os
import subprocess
from pathlib import Path


def print_banner():
    """Print the application banner."""
    print("🤖 Computer-X-Control Quick Launcher")
    print("=" * 50)


def check_dependencies():
    """Check if required dependencies are installed."""
    print("🔍 Checking dependencies...")
    
    dependencies = {
        'pyautogui': 'GUI automation',
        'openai': 'OpenAI GPT support',
        'anthropic': 'Anthropic Claude support',
        'python-dotenv': 'Environment variable support',
        'psutil': 'Process management',
        'pillow': 'Image processing',
        'selenium': 'Web automation'
    }
    
    available = {}
    for dep, description in dependencies.items():
        try:
            __import__(dep.replace('-', '_'))
            available[dep] = True
            print(f"  ✅ {dep}: {description}")
        except ImportError:
            available[dep] = False
            print(f"  ❌ {dep}: {description} (not installed)")
    
    return available


def check_env_file():
    """Check if .env file exists and has API keys."""
    env_file = Path('.env')
    if not env_file.exists():
        print("⚠️  .env file not found")
        return False
    
    # Read .env file and check for API keys
    with open(env_file, 'r') as f:
        content = f.read()
    
    has_openai = 'OPENAI_API_KEY=' in content and 'your_' not in content
    has_anthropic = 'ANTHROPIC_API_KEY=' in content and 'your_' not in content
    
    if has_openai or has_anthropic:
        print("✅ .env file configured with API keys")
        return True
    else:
        print("⚠️  .env file exists but no API keys configured")
        return False


def main():
    """Main launcher function."""
    print_banner()
    
    # Check current directory
    if not Path('main.py').exists():
        print("❌ main.py not found. Please run this script from the Computer-X-Control directory.")
        return 1
    
    # Check dependencies
    deps = check_dependencies()
    has_gui = deps.get('pyautogui', False)
    has_llm = deps.get('openai', False) or deps.get('anthropic', False)
    
    # Check environment
    has_env = check_env_file()
    
    print("\n🎯 Available options:")
    print("1. Run basic tests (no dependencies required)")
    print("2. Run demo (shows how the tool works)")
    
    if has_gui and has_llm and has_env:
        print("3. Interactive mode with LLM (full functionality)")
        print("4. Single command mode")
    else:
        print("3. Interactive mode (disabled - missing dependencies or API keys)")
        print("4. Single command mode (disabled - missing dependencies or API keys)")
    
    print("5. Install dependencies")
    print("6. Setup .env file")
    print("0. Exit")
    
    try:
        choice = input("\n📝 Enter your choice (0-6): ").strip()
        
        if choice == '0':
            print("👋 Goodbye!")
            return 0
        elif choice == '1':
            print("\n🧪 Running basic tests...")
            subprocess.run([sys.executable, 'test_basic.py'])
        elif choice == '2':
            print("\n🎬 Running demo...")
            subprocess.run([sys.executable, 'demo.py'])
        elif choice == '3':
            if has_gui and has_llm and has_env:
                print("\n🚀 Starting interactive mode...")
                subprocess.run([sys.executable, 'main.py'])
            else:
                print("❌ Interactive mode requires GUI, LLM dependencies, and API keys")
                print("   Run option 5 to install dependencies and option 6 to setup API keys")
        elif choice == '4':
            if has_gui and has_llm and has_env:
                command = input("💬 Enter command: ").strip()
                if command:
                    print(f"\n🎯 Executing: {command}")
                    subprocess.run([sys.executable, 'main.py', '-c', command])
            else:
                print("❌ Command mode requires GUI, LLM dependencies, and API keys")
        elif choice == '5':
            print("\n📦 Installing dependencies...")
            if Path('install.sh').exists():
                subprocess.run(['bash', 'install.sh'])
            else:
                print("Running pip install...")
                deps_to_install = [
                    'python-dotenv', 'psutil', 'pyautogui', 'pillow',
                    'opencv-python', 'openai', 'anthropic', 'selenium', 'webdriver-manager'
                ]
                subprocess.run([sys.executable, '-m', 'pip', 'install'] + deps_to_install)
        elif choice == '6':
            print("\n⚙️  Setting up .env file...")
            if not Path('.env').exists():
                subprocess.run(['cp', '.env.example', '.env'])
                print("✅ .env file created from template")
            print("📝 Please edit .env file and add your API keys:")
            print("   - Get OpenAI API key from: https://platform.openai.com/api-keys")
            print("   - Get Anthropic API key from: https://console.anthropic.com/")
            
            # Open .env file in default editor
            env_path = Path('.env').absolute()
            if os.name == 'nt':  # Windows
                os.startfile(env_path)
            elif os.name == 'posix':  # Linux/Mac
                subprocess.run(['xdg-open', env_path], capture_output=True)
                # Fallback to nano if xdg-open fails
                if subprocess.run(['which', 'nano'], capture_output=True).returncode == 0:
                    subprocess.run(['nano', env_path])
                else:
                    print(f"📄 Please manually edit: {env_path}")
        else:
            print("❌ Invalid choice")
            
    except KeyboardInterrupt:
        print("\n👋 Interrupted by user. Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())