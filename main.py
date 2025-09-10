#!/usr/bin/env python3
"""
Computer-X-Control Main Application

A tool that allows Large Language Models to control PC operations through
natural language commands.
"""

import sys
import os
import json
import argparse
from pathlib import Path
from typing import Optional

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from computer_x_control.automation.pc_controller import PCController
from computer_x_control.llm.llm_interface import LLMInterface
from computer_x_control.parser.command_parser import CommandParser


class ComputerXControl:
    """Main application class for Computer-X-Control."""
    
    def __init__(self, llm_provider: str = "openai", safety_mode: bool = True):
        """
        Initialize the Computer-X-Control application.
        
        Args:
            llm_provider: LLM provider to use ('openai' or 'anthropic')
            safety_mode: Enable safety checks
        """
        self.safety_mode = safety_mode
        
        # Initialize components
        try:
            self.pc_controller = PCController(safety_mode=safety_mode)
            self.llm_interface = LLMInterface(provider=llm_provider)
            self.command_parser = CommandParser(self.pc_controller)
            print(f"✅ Computer-X-Control initialized with {llm_provider.upper()} LLM")
        except Exception as e:
            print(f"❌ Failed to initialize: {e}")
            sys.exit(1)
    
    def process_command(self, user_input: str, context: Optional[str] = None) -> dict:
        """
        Process a natural language command.
        
        Args:
            user_input: Natural language command from user
            context: Optional context information
            
        Returns:
            Dictionary with execution results
        """
        print(f"🎯 Processing command: {user_input}")
        
        # Parse command using LLM
        parsed_command = self.llm_interface.parse_command(user_input, context)
        
        if parsed_command.get('action') == 'error':
            return {
                'success': False,
                'error': parsed_command.get('error', 'Unknown error'),
                'stage': 'llm_parsing'
            }
        
        print(f"🧠 LLM parsed command: {json.dumps(parsed_command, indent=2)}")
        
        # Validate command
        if not self.command_parser.validate_command(parsed_command):
            return {
                'success': False,
                'error': 'Invalid command structure',
                'stage': 'validation',
                'parsed_command': parsed_command
            }
        
        # Execute command
        result = self.command_parser.execute_command(parsed_command)
        
        if result.get('success'):
            print(f"✅ Command executed successfully: {result.get('details', 'No details')}")
        else:
            print(f"❌ Command failed: {result.get('error', 'Unknown error')}")
        
        return result
    
    def interactive_mode(self):
        """Run in interactive mode for continuous command processing."""
        print("🚀 Computer-X-Control Interactive Mode")
        print("Type your commands in natural language. Type 'quit' or 'exit' to stop.")
        print("Example commands:")
        print("  - 'Take a screenshot'")
        print("  - 'Open notepad'")
        print("  - 'Click at position 100, 200'")
        print("  - 'Type hello world'")
        print("  - 'Press enter key'")
        print("-" * 50)
        
        while True:
            try:
                user_input = input("\n💬 Enter command: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'stop']:
                    print("👋 Goodbye!")
                    break
                
                if not user_input:
                    continue
                
                result = self.process_command(user_input)
                
                # Handle clarification requests
                if result.get('action') == 'clarify':
                    print(f"❓ {result.get('message', 'Need clarification')}")
                    continue
                
                # Display results
                if result.get('success'):
                    if result.get('screenshot_path'):
                        print(f"📸 Screenshot saved: {result['screenshot_path']}")
                    if result.get('output'):
                        print(f"📄 Output: {result['output']}")
                else:
                    print(f"🔥 Error: {result.get('error', 'Unknown error')}")
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"💥 Unexpected error: {e}")
    
    def execute_file(self, file_path: str):
        """
        Execute commands from a file.
        
        Args:
            file_path: Path to file containing commands
        """
        try:
            with open(file_path, 'r') as f:
                commands = f.readlines()
            
            print(f"📄 Executing {len(commands)} commands from {file_path}")
            
            for i, command in enumerate(commands, 1):
                command = command.strip()
                if not command or command.startswith('#'):
                    continue
                
                print(f"\n📋 Command {i}: {command}")
                result = self.process_command(command)
                
                if not result.get('success'):
                    print(f"💥 Stopping execution due to error: {result.get('error')}")
                    break
                    
        except FileNotFoundError:
            print(f"❌ File not found: {file_path}")
        except Exception as e:
            print(f"💥 Error executing file: {e}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Computer-X-Control: LLM-powered PC automation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                          # Interactive mode
  python main.py -c "take a screenshot"   # Single command
  python main.py -f commands.txt          # Execute from file
  python main.py --llm anthropic          # Use Anthropic Claude
        """
    )
    
    parser.add_argument(
        '--llm', 
        choices=['openai', 'anthropic'], 
        default='openai',
        help='LLM provider to use (default: openai)'
    )
    
    parser.add_argument(
        '--no-safety',
        action='store_true',
        help='Disable safety mode (use with caution)'
    )
    
    parser.add_argument(
        '-c', '--command',
        type=str,
        help='Execute a single command'
    )
    
    parser.add_argument(
        '-f', '--file',
        type=str,
        help='Execute commands from a file'
    )
    
    args = parser.parse_args()
    
    # Check if .env file exists
    env_file = Path('.env')
    if not env_file.exists():
        print("⚠️  No .env file found. Please create one based on .env.example")
        print("   You need to add your LLM API keys to use this tool.")
        return
    
    # Initialize application
    safety_mode = not args.no_safety
    app = ComputerXControl(llm_provider=args.llm, safety_mode=safety_mode)
    
    if safety_mode:
        print("🛡️  Safety mode enabled (dangerous commands blocked)")
    else:
        print("⚠️  Safety mode disabled - be careful!")
    
    # Execute based on arguments
    if args.command:
        result = app.process_command(args.command)
        if not result.get('success'):
            sys.exit(1)
    elif args.file:
        app.execute_file(args.file)
    else:
        app.interactive_mode()


if __name__ == "__main__":
    main()