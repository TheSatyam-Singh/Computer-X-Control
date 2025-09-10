"""
LLM Interface Module

Handles communication with various LLM providers (OpenAI, Anthropic) to
interpret user commands and generate PC control actions.
"""

import os
import json
from typing import Dict, List, Optional, Any

# Try to load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False
    print("⚠️  python-dotenv not available - using system environment variables only")

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False


class LLMInterface:
    """Interface for communicating with Large Language Models."""
    
    def __init__(self, provider: str = "openai", model: str = None):
        """
        Initialize LLM interface.
        
        Args:
            provider: LLM provider ('openai' or 'anthropic')
            model: Specific model to use
        """
        self.provider = provider.lower()
        self.model = model
        self.client = None
        
        # Initialize the appropriate client
        if self.provider == "openai" and OPENAI_AVAILABLE:
            self._init_openai()
        elif self.provider == "anthropic" and ANTHROPIC_AVAILABLE:
            self._init_anthropic()
        else:
            raise ValueError(f"Provider '{provider}' not available or not installed")
    
    def _init_openai(self):
        """Initialize OpenAI client."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        self.client = openai.OpenAI(api_key=api_key)
        if not self.model:
            self.model = "gpt-3.5-turbo"
    
    def _init_anthropic(self):
        """Initialize Anthropic client."""
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
        
        self.client = anthropic.Anthropic(api_key=api_key)
        if not self.model:
            self.model = "claude-3-sonnet-20240229"
    
    def parse_command(self, user_input: str, context: Optional[str] = None) -> Dict[str, Any]:
        """
        Parse a natural language command into PC control actions.
        
        Args:
            user_input: Natural language command from user
            context: Optional context information
            
        Returns:
            Dictionary containing parsed command information
        """
        system_prompt = self._get_system_prompt()
        
        # Create the user message with context if provided
        user_message = user_input
        if context:
            user_message = f"Context: {context}\n\nCommand: {user_input}"
        
        try:
            if self.provider == "openai":
                response = self._call_openai(system_prompt, user_message)
            elif self.provider == "anthropic":
                response = self._call_anthropic(system_prompt, user_message)
            else:
                raise ValueError(f"Unknown provider: {self.provider}")
            
            # Parse the JSON response
            try:
                parsed_response = json.loads(response)
                return parsed_response
            except json.JSONDecodeError:
                # If JSON parsing fails, return a fallback response
                return {
                    "action": "error",
                    "error": "Failed to parse LLM response as JSON",
                    "raw_response": response
                }
                
        except Exception as e:
            return {
                "action": "error",
                "error": str(e)
            }
    
    def _call_openai(self, system_prompt: str, user_message: str) -> str:
        """Call OpenAI API."""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.1,
            max_tokens=1000
        )
        return response.choices[0].message.content
    
    def _call_anthropic(self, system_prompt: str, user_message: str) -> str:
        """Call Anthropic API."""
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1000,
            temperature=0.1,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_message}
            ]
        )
        return response.content[0].text
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for PC control command parsing."""
        return """You are a PC automation assistant. Parse user commands into JSON actions that can control a computer.

Available actions:
- click: Click at coordinates {"action": "click", "x": 100, "y": 200, "button": "left", "clicks": 1}
- type: Type text {"action": "type", "text": "hello world", "interval": 0.05}
- key: Press keys {"action": "key", "key": "enter"} or {"action": "key", "key": "ctrl+c"}
- scroll: Scroll {"action": "scroll", "direction": "up", "clicks": 3}
- screenshot: Take screenshot {"action": "screenshot", "filename": "optional.png"}
- open_app: Open application {"action": "open_app", "app_name": "notepad"}
- command: Run system command {"action": "command", "command": "dir"}
- move_mouse: Move mouse {"action": "move_mouse", "x": 100, "y": 200, "duration": 0.5}
- drag: Drag mouse {"action": "drag", "start_x": 100, "start_y": 200, "end_x": 300, "end_y": 400}
- wait: Wait {"action": "wait", "seconds": 2.0}
- multiple: Multiple actions {"action": "multiple", "actions": [action1, action2, ...]}

For unclear commands, ask for clarification: {"action": "clarify", "message": "What do you want me to do?"}

Always respond with valid JSON only. No explanations outside the JSON."""

    def get_clarification(self, original_command: str, clarification_request: str) -> str:
        """
        Get clarification for an unclear command.
        
        Args:
            original_command: The original user command
            clarification_request: What needs to be clarified
            
        Returns:
            Clarification message for the user
        """
        return f"I need clarification for: '{original_command}'\n\n{clarification_request}"