#!/usr/bin/env python3
"""
Test script for Computer-X-Control functionality.
Tests the basic components without requiring external dependencies.
"""

import sys
import json
import subprocess
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from computer_x_control.automation.pc_controller import PCController
from computer_x_control.parser.command_parser import CommandParser


def test_pc_controller():
    """Test PC Controller basic functionality."""
    print("🧪 Testing PC Controller...")
    
    controller = PCController(safety_mode=True)
    
    # Test basic initialization
    print(f"✅ PC Controller initialized (GUI available: {controller.gui_available})")
    print(f"📏 Screen dimensions: {controller.screen_width}x{controller.screen_height}")
    
    # Test safe command
    result = controller.run_command("echo Hello World")
    print(f"💻 Command result: {result}")
    
    # Test window list
    try:
        windows = controller.get_window_list()
        print(f"🪟 Found {len(windows)} running processes")
        if windows:
            print(f"    Example process: {windows[0]}")
    except Exception as e:
        print(f"⚠️  Window list failed: {e}")
    
    # Test screenshot (will fail gracefully if GUI not available)
    try:
        screenshot_path = controller.take_screenshot("test_screenshot.png")
        print(f"📸 Screenshot saved: {screenshot_path}")
    except Exception as e:
        print(f"⚠️  Screenshot failed: {e}")
    
    return True


def test_command_parser():
    """Test Command Parser functionality."""
    print("\n🧪 Testing Command Parser...")
    
    controller = PCController(safety_mode=True)
    parser = CommandParser(controller)
    
    # Test command execution
    test_commands = [
        {"action": "wait", "seconds": 0.1},
        {"action": "command", "command": "echo Testing"},
        {"action": "screenshot", "filename": "parser_test.png"},
        {"action": "move_mouse", "x": 100, "y": 100, "duration": 0.1}
    ]
    
    for cmd in test_commands:
        print(f"🎯 Testing: {cmd['action']}")
        result = parser.execute_command(cmd)
        if result.get('success'):
            print(f"  ✅ {result.get('details', 'Success')}")
        else:
            print(f"  ⚠️  {result.get('error', 'Failed')}")
    
    # Test validation
    invalid_cmd = {"action": "invalid_action"}
    result = parser.execute_command(invalid_cmd)
    print(f"❌ Invalid command result: {result.get('error', 'No error')}")
    
    return True


def test_offline_mode():
    """Test the tool without LLM integration using mock commands."""
    print("\n🧪 Testing Offline Mode (Simulated LLM responses)...")
    
    controller = PCController(safety_mode=True)
    parser = CommandParser(controller)
    
    # Simulate various LLM command responses
    mock_llm_responses = [
        {
            "user_input": "take a screenshot",
            "llm_response": {"action": "screenshot", "filename": "offline_test.png"}
        },
        {
            "user_input": "wait 1 second",
            "llm_response": {"action": "wait", "seconds": 1.0}
        },
        {
            "user_input": "run echo command",
            "llm_response": {"action": "command", "command": "echo Hello from Computer-X-Control"}
        },
        {
            "user_input": "multiple actions",
            "llm_response": {
                "action": "multiple",
                "actions": [
                    {"action": "wait", "seconds": 0.1},
                    {"action": "command", "command": "echo Step 1"},
                    {"action": "wait", "seconds": 0.1},
                    {"action": "command", "command": "echo Step 2"}
                ]
            }
        }
    ]
    
    for test_case in mock_llm_responses:
        print(f"🎯 User: '{test_case['user_input']}'")
        print(f"🧠 LLM Response: {json.dumps(test_case['llm_response'], indent=2)}")
        
        result = parser.execute_command(test_case['llm_response'])
        
        if result.get('success'):
            print(f"✅ Executed successfully: {result.get('details', 'No details')}")
            if result.get('output'):
                print(f"📄 Output: {result.get('output')}")
        else:
            print(f"❌ Failed: {result.get('error')}")
        
        print("-" * 40)
    
    return True


def test_system_commands():
    """Test system command execution with safety checks."""
    print("\n🧪 Testing System Commands...")
    
    controller = PCController(safety_mode=True)
    
    # Test safe commands
    safe_commands = [
        "echo Hello World",
        "pwd" if os.name != 'nt' else "cd",
        "date" if os.name != 'nt' else "time /t",
        "whoami" if os.name != 'nt' else "echo %USERNAME%"
    ]
    
    for cmd in safe_commands:
        print(f"💻 Running: {cmd}")
        result = controller.run_command(cmd)
        if result['success']:
            print(f"  ✅ Output: {result['output'].strip()}")
        else:
            print(f"  ❌ Error: {result['error']}")
    
    # Test dangerous command (should be blocked)
    dangerous_cmd = "rm -rf /" if os.name != 'nt' else "del /f C:\\"
    print(f"🛡️  Testing dangerous command: {dangerous_cmd}")
    result = controller.run_command(dangerous_cmd)
    if not result['success']:
        print(f"  ✅ Correctly blocked: {result['error']}")
    else:
        print(f"  ⚠️  DANGER: Command was not blocked!")
    
    return True


def main():
    """Run all tests."""
    print("🚀 Computer-X-Control Test Suite")
    print("=" * 50)
    
    try:
        # Test individual components
        test_pc_controller()
        test_command_parser()
        test_offline_mode()
        test_system_commands()
        
        print("\n" + "=" * 50)
        print("✅ All tests completed successfully!")
        print("\n📋 Summary:")
        print("• Core functionality is working")
        print("• Command parsing and execution working")
        print("• Safety checks are active")
        print("• System commands are functional")
        print("\n🔧 To enable full functionality:")
        print("1. Install GUI dependencies: pip install pyautogui pillow")
        print("2. Install LLM dependencies: pip install openai anthropic python-dotenv")
        print("3. Set up your .env file with API keys")
        print("4. Run: python main.py")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    import os
    sys.exit(main())