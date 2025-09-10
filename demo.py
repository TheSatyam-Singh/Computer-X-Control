#!/usr/bin/env python3
"""
Computer-X-Control Demo Script

Demonstrates the capabilities of the Computer-X-Control tool
without requiring LLM API keys by using pre-generated command examples.
"""

import sys
import json
import time
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from computer_x_control.automation.pc_controller import PCController
from computer_x_control.parser.command_parser import CommandParser


class DemoRunner:
    """Demonstration runner for Computer-X-Control."""
    
    def __init__(self):
        self.controller = PCController(safety_mode=True)
        self.parser = CommandParser(self.controller)
        
    def run_demo(self):
        """Run the complete demonstration."""
        print("🚀 Computer-X-Control Demonstration")
        print("=" * 60)
        print("This demo shows how an LLM would control your PC through")
        print("natural language commands translated to specific actions.")
        print("=" * 60)
        
        # Demo scenarios
        scenarios = [
            self.demo_basic_commands,
            self.demo_system_operations,
            self.demo_complex_workflows,
            self.demo_safety_features
        ]
        
        for i, scenario in enumerate(scenarios, 1):
            print(f"\n🎯 Demo {i}: {scenario.__name__.replace('demo_', '').replace('_', ' ').title()}")
            print("-" * 40)
            scenario()
            
            if i < len(scenarios):
                input("\n⏸️  Press Enter to continue to next demo...")
        
        print("\n" + "=" * 60)
        print("✅ Demo completed! This shows how Computer-X-Control works:")
        print("1. User gives natural language command")
        print("2. LLM translates to JSON action format")
        print("3. Command parser executes the action safely")
        print("4. Results are returned to user")
        print("\n🔧 To use with real LLM integration:")
        print("• Install dependencies: pip install pyautogui openai anthropic python-dotenv")
        print("• Set up API keys in .env file")
        print("• Run: python main.py")
    
    def demo_basic_commands(self):
        """Demonstrate basic command execution."""
        examples = [
            {
                "user_input": "Show me the current date and time",
                "llm_response": {"action": "command", "command": "date"},
                "explanation": "LLM translates request to system command"
            },
            {
                "user_input": "Wait for 2 seconds",
                "llm_response": {"action": "wait", "seconds": 2.0},
                "explanation": "Simple wait command for timing control"
            },
            {
                "user_input": "Show me the current directory",
                "llm_response": {"action": "command", "command": "pwd"},
                "explanation": "Directory navigation command"
            }
        ]
        
        self._run_examples(examples)
    
    def demo_system_operations(self):
        """Demonstrate system operations."""
        examples = [
            {
                "user_input": "List running processes",
                "llm_response": {"action": "command", "command": "ps aux | head -10"},
                "explanation": "System monitoring command"
            },
            {
                "user_input": "Check disk space",
                "llm_response": {"action": "command", "command": "df -h"},
                "explanation": "System resource monitoring"
            },
            {
                "user_input": "Show my username",
                "llm_response": {"action": "command", "command": "whoami"},
                "explanation": "User information command"
            }
        ]
        
        self._run_examples(examples)
    
    def demo_complex_workflows(self):
        """Demonstrate complex multi-step workflows."""
        examples = [
            {
                "user_input": "Create a test file, write hello to it, then show its contents",
                "llm_response": {
                    "action": "multiple",
                    "actions": [
                        {"action": "command", "command": "echo 'Hello from Computer-X-Control!' > /tmp/test_file.txt"},
                        {"action": "wait", "seconds": 0.5},
                        {"action": "command", "command": "cat /tmp/test_file.txt"},
                        {"action": "wait", "seconds": 0.5},
                        {"action": "command", "command": "rm /tmp/test_file.txt"}
                    ]
                },
                "explanation": "Multi-step workflow with file operations"
            },
            {
                "user_input": "Check system info step by step",
                "llm_response": {
                    "action": "multiple", 
                    "actions": [
                        {"action": "command", "command": "echo 'System Information:'"},
                        {"action": "wait", "seconds": 0.5},
                        {"action": "command", "command": "uname -a"},
                        {"action": "wait", "seconds": 0.5},
                        {"action": "command", "command": "echo 'Current user:'"},
                        {"action": "command", "command": "whoami"}
                    ]
                },
                "explanation": "Sequential information gathering"
            }
        ]
        
        self._run_examples(examples)
    
    def demo_safety_features(self):
        """Demonstrate safety features."""
        print("🛡️  Testing Safety Features:")
        print("Computer-X-Control blocks dangerous commands in safety mode.")
        
        dangerous_examples = [
            {
                "user_input": "Delete all files (DANGEROUS - will be blocked)",
                "llm_response": {"action": "command", "command": "rm -rf /"},
                "explanation": "Dangerous command blocked by safety mode"
            },
            {
                "user_input": "Shutdown the computer (DANGEROUS - will be blocked)",
                "llm_response": {"action": "command", "command": "shutdown -h now"},
                "explanation": "System shutdown blocked by safety mode"
            }
        ]
        
        for example in dangerous_examples:
            print(f"\n💬 User: \"{example['user_input']}\"")
            print(f"🧠 LLM Response: {json.dumps(example['llm_response'], indent=2)}")
            print(f"💡 Explanation: {example['explanation']}")
            
            result = self.parser.execute_command(example['llm_response'])
            
            if result.get('success'):
                print("⚠️  WARNING: Dangerous command was NOT blocked!")
            else:
                print(f"✅ Safety Check: {result.get('error')}")
        
        # Show that safe commands still work
        print(f"\n💬 User: \"Show me a safe command works\"")
        safe_cmd = {"action": "command", "command": "echo 'Safety mode is working correctly!'"}
        print(f"🧠 LLM Response: {json.dumps(safe_cmd, indent=2)}")
        result = self.parser.execute_command(safe_cmd)
        if result.get('success'):
            print(f"✅ Safe Command: {result.get('output', '').strip()}")
    
    def _run_examples(self, examples):
        """Run a list of example commands."""
        for example in examples:
            print(f"\n💬 User: \"{example['user_input']}\"")
            print(f"🧠 LLM Response: {json.dumps(example['llm_response'], indent=2)}")
            print(f"💡 Explanation: {example['explanation']}")
            
            result = self.parser.execute_command(example['llm_response'])
            
            if result.get('success'):
                print(f"✅ Executed: {result.get('details', 'Success')}")
                if result.get('output'):
                    output = result.get('output', '').strip()
                    if len(output) > 200:
                        output = output[:200] + "..."
                    print(f"📄 Output: {output}")
            else:
                print(f"❌ Failed: {result.get('error')}")
            
            time.sleep(0.5)  # Small delay for readability


def main():
    """Main demo function."""
    print("Welcome to Computer-X-Control Demo!")
    print("This demonstration shows how the tool works without requiring LLM API keys.")
    print("\nPress Ctrl+C at any time to exit.")
    
    try:
        demo = DemoRunner()
        demo.run_demo()
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()