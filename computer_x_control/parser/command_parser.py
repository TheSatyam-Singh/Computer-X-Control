"""
Command Parser Module

Parses LLM responses and executes the corresponding PC control actions.
"""

import json
import time
from typing import Dict, Any, List, Optional
from ..automation.pc_controller import PCController


class CommandParser:
    """Parser for executing LLM-generated PC control commands."""
    
    def __init__(self, pc_controller: PCController):
        """
        Initialize command parser.
        
        Args:
            pc_controller: Instance of PCController for executing actions
        """
        self.pc_controller = pc_controller
        
        # Map action names to methods
        self.action_map = {
            'click': self._execute_click,
            'type': self._execute_type,
            'key': self._execute_key,
            'scroll': self._execute_scroll,
            'screenshot': self._execute_screenshot,
            'open_app': self._execute_open_app,
            'command': self._execute_command,
            'move_mouse': self._execute_move_mouse,
            'drag': self._execute_drag,
            'wait': self._execute_wait,
            'multiple': self._execute_multiple,
            'clarify': self._execute_clarify,
            'error': self._execute_error
        }
    
    def execute_command(self, command_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a parsed command.
        
        Args:
            command_data: Dictionary containing command information
            
        Returns:
            Execution result dictionary
        """
        action = command_data.get('action', '').lower()
        
        if action not in self.action_map:
            return {
                'success': False,
                'error': f"Unknown action: {action}",
                'action': action
            }
        
        try:
            return self.action_map[action](command_data)
        except Exception as e:
            return {
                'success': False,
                'error': f"Execution failed: {str(e)}",
                'action': action
            }
    
    def _execute_click(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute click action."""
        x = data.get('x', 0)
        y = data.get('y', 0)
        button = data.get('button', 'left')
        clicks = data.get('clicks', 1)
        
        success = self.pc_controller.click(x, y, button, clicks)
        
        return {
            'success': success,
            'action': 'click',
            'details': f"Clicked at ({x}, {y}) with {button} button, {clicks} times"
        }
    
    def _execute_type(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute type action."""
        text = data.get('text', '')
        interval = data.get('interval', 0.05)
        
        success = self.pc_controller.type_text(text, interval)
        
        return {
            'success': success,
            'action': 'type',
            'details': f"Typed: '{text}'"
        }
    
    def _execute_key(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute key press action."""
        key = data.get('key', '')
        presses = data.get('presses', 1)
        
        success = self.pc_controller.press_key(key, presses)
        
        return {
            'success': success,
            'action': 'key',
            'details': f"Pressed key: '{key}' {presses} times"
        }
    
    def _execute_scroll(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute scroll action."""
        direction = data.get('direction', 'up')
        clicks = data.get('clicks', 3)
        
        success = self.pc_controller.scroll(direction, clicks)
        
        return {
            'success': success,
            'action': 'scroll',
            'details': f"Scrolled {direction} {clicks} clicks"
        }
    
    def _execute_screenshot(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute screenshot action."""
        filename = data.get('filename')
        
        try:
            screenshot_path = self.pc_controller.take_screenshot(filename)
            return {
                'success': True,
                'action': 'screenshot',
                'details': f"Screenshot saved to: {screenshot_path}",
                'screenshot_path': screenshot_path
            }
        except Exception as e:
            return {
                'success': False,
                'action': 'screenshot',
                'error': str(e)
            }
    
    def _execute_open_app(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute open application action."""
        app_name = data.get('app_name', '')
        
        success = self.pc_controller.open_application(app_name)
        
        return {
            'success': success,
            'action': 'open_app',
            'details': f"Opened application: {app_name}"
        }
    
    def _execute_command(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute system command action."""
        command = data.get('command', '')
        
        result = self.pc_controller.run_command(command)
        
        return {
            'success': result['success'],
            'action': 'command',
            'details': f"Executed command: {command}",
            'output': result['output'],
            'error': result['error'],
            'return_code': result['return_code']
        }
    
    def _execute_move_mouse(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute move mouse action."""
        x = data.get('x', 0)
        y = data.get('y', 0)
        duration = data.get('duration', 0.5)
        
        success = self.pc_controller.move_mouse(x, y, duration)
        
        return {
            'success': success,
            'action': 'move_mouse',
            'details': f"Moved mouse to ({x}, {y}) in {duration}s"
        }
    
    def _execute_drag(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute drag action."""
        start_x = data.get('start_x', 0)
        start_y = data.get('start_y', 0)
        end_x = data.get('end_x', 0)
        end_y = data.get('end_y', 0)
        duration = data.get('duration', 1.0)
        
        success = self.pc_controller.drag_mouse(start_x, start_y, end_x, end_y, duration)
        
        return {
            'success': success,
            'action': 'drag',
            'details': f"Dragged from ({start_x}, {start_y}) to ({end_x}, {end_y})"
        }
    
    def _execute_wait(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute wait action."""
        seconds = data.get('seconds', 1.0)
        
        self.pc_controller.wait(seconds)
        
        return {
            'success': True,
            'action': 'wait',
            'details': f"Waited {seconds} seconds"
        }
    
    def _execute_multiple(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute multiple actions sequentially."""
        actions = data.get('actions', [])
        results = []
        
        for action in actions:
            result = self.execute_command(action)
            results.append(result)
            
            # Stop if any action fails
            if not result.get('success', False):
                break
        
        success = all(result.get('success', False) for result in results)
        
        return {
            'success': success,
            'action': 'multiple',
            'details': f"Executed {len(results)} actions",
            'results': results
        }
    
    def _execute_clarify(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle clarification request."""
        message = data.get('message', 'Need clarification')
        
        return {
            'success': True,
            'action': 'clarify',
            'message': message,
            'details': "Clarification requested"
        }
    
    def _execute_error(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle error from LLM."""
        error = data.get('error', 'Unknown error')
        
        return {
            'success': False,
            'action': 'error',
            'error': error,
            'details': "LLM returned an error"
        }
    
    def validate_command(self, command_data: Dict[str, Any]) -> bool:
        """
        Validate a command before execution.
        
        Args:
            command_data: Command to validate
            
        Returns:
            True if command is valid
        """
        if not isinstance(command_data, dict):
            return False
        
        action = command_data.get('action')
        if not action or action not in self.action_map:
            return False
        
        # Add specific validation for each action type
        if action == 'click':
            return 'x' in command_data and 'y' in command_data
        elif action == 'type':
            return 'text' in command_data
        elif action == 'key':
            return 'key' in command_data
        elif action == 'open_app':
            return 'app_name' in command_data
        elif action == 'command':
            return 'command' in command_data
        elif action == 'multiple':
            return 'actions' in command_data and isinstance(command_data['actions'], list)
        
        # Default to True for other actions
        return True