"""
PC Controller Module

Handles all PC automation tasks including GUI control, file operations,
system commands, and web automation.
"""

import subprocess
import os
import time
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

# Try to import optional dependencies
try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False
    print("⚠️  PyAutoGUI not available - GUI automation disabled")

try:
    import cv2
    import numpy as np
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    print("⚠️  psutil not available - process listing limited")


class PCController:
    """Main class for controlling PC operations through automation."""
    
    def __init__(self, safety_mode: bool = True):
        """
        Initialize PC Controller.
        
        Args:
            safety_mode: Enable safety checks to prevent dangerous operations
        """
        self.safety_mode = safety_mode
        self.screenshot_dir = Path("screenshots")
        self.screenshot_dir.mkdir(exist_ok=True)
        
        # Check if GUI automation is available
        if not PYAUTOGUI_AVAILABLE:
            print("⚠️  GUI automation features disabled (PyAutoGUI not installed)")
            self.gui_available = False
            self.screen_width = 1920  # Default fallback
            self.screen_height = 1080  # Default fallback
        else:
            self.gui_available = True
            # Configure pyautogui safety settings
            pyautogui.FAILSAFE = True  # Move mouse to corner to abort
            pyautogui.PAUSE = 0.5  # Pause between actions
            
            # Get screen dimensions
            self.screen_width, self.screen_height = pyautogui.size()
        
        # Dangerous commands that require confirmation
        self.dangerous_commands = [
            'shutdown', 'restart', 'reboot', 'format', 'delete', 'rm -rf',
            'del /f', 'rmdir /s', 'registry', 'regedit'
        ]
    
    def take_screenshot(self, filename: Optional[str] = None) -> str:
        """
        Take a screenshot of the current screen.
        
        Args:
            filename: Optional filename for the screenshot
            
        Returns:
            Path to the saved screenshot
        """
        if not self.gui_available:
            raise RuntimeError("Screenshot functionality requires PyAutoGUI")
            
        if filename is None:
            timestamp = int(time.time())
            filename = f"screenshot_{timestamp}.png"
        
        screenshot_path = self.screenshot_dir / filename
        screenshot = pyautogui.screenshot()
        screenshot.save(screenshot_path)
        
        return str(screenshot_path)
    
    def click(self, x: int, y: int, button: str = 'left', clicks: int = 1) -> bool:
        """
        Click at specified coordinates.
        
        Args:
            x: X coordinate
            y: Y coordinate  
            button: Mouse button ('left', 'right', 'middle')
            clicks: Number of clicks
            
        Returns:
            Success status
        """
        if not self.gui_available:
            print("⚠️  GUI automation not available (PyAutoGUI not installed)")
            return False
            
        try:
            if not self._validate_coordinates(x, y):
                return False
                
            pyautogui.click(x, y, clicks=clicks, button=button)
            return True
        except Exception as e:
            print(f"Click failed: {e}")
            return False
    
    def type_text(self, text: str, interval: float = 0.05) -> bool:
        """
        Type text at current cursor position.
        
        Args:
            text: Text to type
            interval: Interval between keystrokes
            
        Returns:
            Success status
        """
        if not self.gui_available:
            print("⚠️  GUI automation not available (PyAutoGUI not installed)")
            return False
            
        try:
            pyautogui.typewrite(text, interval=interval)
            return True
        except Exception as e:
            print(f"Type text failed: {e}")
            return False
    
    def press_key(self, key: str, presses: int = 1) -> bool:
        """
        Press a key or key combination.
        
        Args:
            key: Key to press (e.g., 'enter', 'ctrl+c', 'alt+tab')
            presses: Number of times to press
            
        Returns:
            Success status
        """
        if not self.gui_available:
            print("⚠️  GUI automation not available (PyAutoGUI not installed)")
            return False
            
        try:
            if '+' in key:
                # Handle key combinations
                keys = key.split('+')
                pyautogui.hotkey(*keys)
            else:
                pyautogui.press(key, presses=presses)
            return True
        except Exception as e:
            print(f"Key press failed: {e}")
            return False
    
    def scroll(self, direction: str, clicks: int = 3) -> bool:
        """
        Scroll in specified direction.
        
        Args:
            direction: 'up' or 'down'
            clicks: Number of scroll clicks
            
        Returns:
            Success status
        """
        if not self.gui_available:
            print("⚠️  GUI automation not available (PyAutoGUI not installed)")
            return False
            
        try:
            scroll_amount = clicks if direction == 'up' else -clicks
            pyautogui.scroll(scroll_amount)
            return True
        except Exception as e:
            print(f"Scroll failed: {e}")
            return False
    
    def find_image_on_screen(self, image_path: str, confidence: float = 0.8) -> Optional[Tuple[int, int]]:
        """
        Find an image on the screen and return its center coordinates.
        
        Args:
            image_path: Path to the image to find
            confidence: Confidence threshold for image matching
            
        Returns:
            Tuple of (x, y) coordinates or None if not found
        """
        if not self.gui_available:
            print("⚠️  Image recognition not available (PyAutoGUI not installed)")
            return None
            
        try:
            location = pyautogui.locateOnScreen(image_path, confidence=confidence)
            if location:
                center = pyautogui.center(location)
                return center.x, center.y
            return None
        except Exception as e:
            print(f"Image search failed: {e}")
            return None
    
    def open_application(self, app_name: str) -> bool:
        """
        Open an application by name.
        
        Args:
            app_name: Name or path of the application
            
        Returns:
            Success status
        """
        try:
            if os.name == 'nt':  # Windows
                subprocess.Popen(['start', app_name], shell=True)
            else:  # Linux/Mac
                subprocess.Popen([app_name])
            return True
        except Exception as e:
            print(f"Failed to open application: {e}")
            return False
    
    def run_command(self, command: str, shell: bool = True) -> Dict[str, Any]:
        """
        Execute a system command.
        
        Args:
            command: Command to execute
            shell: Whether to use shell
            
        Returns:
            Dictionary with result information
        """
        if self.safety_mode and self._is_dangerous_command(command):
            return {
                'success': False,
                'error': 'Command blocked by safety mode',
                'output': '',
                'return_code': -1
            }
        
        try:
            result = subprocess.run(
                command,
                shell=shell,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            return {
                'success': result.returncode == 0,
                'output': result.stdout,
                'error': result.stderr,
                'return_code': result.returncode
            }
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': 'Command timed out',
                'output': '',
                'return_code': -1
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'output': '',
                'return_code': -1
            }
    
    def get_window_list(self) -> List[Dict[str, Any]]:
        """
        Get list of open windows.
        
        Returns:
            List of window information dictionaries
        """
        windows = []
        try:
            if PSUTIL_AVAILABLE:
                for proc in psutil.process_iter(['pid', 'name', 'exe']):
                    try:
                        process_info = proc.info
                        if process_info['name']:
                            windows.append({
                                'pid': process_info['pid'],
                                'name': process_info['name'],
                                'exe': process_info['exe'] or 'Unknown'
                            })
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue
            else:
                # Fallback using built-in methods
                if os.name == 'nt':  # Windows
                    result = subprocess.run(['tasklist'], capture_output=True, text=True)
                    if result.returncode == 0:
                        lines = result.stdout.split('\n')[3:]  # Skip header
                        for line in lines:
                            parts = line.split()
                            if len(parts) >= 2:
                                windows.append({
                                    'pid': parts[1] if parts[1].isdigit() else 'Unknown',
                                    'name': parts[0],
                                    'exe': parts[0]
                                })
                else:  # Linux/Mac
                    result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
                    if result.returncode == 0:
                        lines = result.stdout.split('\n')[1:]  # Skip header
                        for line in lines:
                            parts = line.split()
                            if len(parts) >= 11:
                                windows.append({
                                    'pid': parts[1],
                                    'name': parts[10],
                                    'exe': parts[10]
                                })
        except Exception as e:
            print(f"Failed to get window list: {e}")
        
        return windows
    
    def move_mouse(self, x: int, y: int, duration: float = 0.5) -> bool:
        """
        Move mouse to specified coordinates.
        
        Args:
            x: X coordinate
            y: Y coordinate
            duration: Duration of movement in seconds
            
        Returns:
            Success status
        """
        if not self.gui_available:
            print("⚠️  GUI automation not available (PyAutoGUI not installed)")
            return False
            
        try:
            if not self._validate_coordinates(x, y):
                return False
                
            pyautogui.moveTo(x, y, duration=duration)
            return True
        except Exception as e:
            print(f"Mouse move failed: {e}")
            return False
    
    def drag_mouse(self, start_x: int, start_y: int, end_x: int, end_y: int, 
                   duration: float = 1.0) -> bool:
        """
        Drag mouse from start to end coordinates.
        
        Args:
            start_x: Starting X coordinate
            start_y: Starting Y coordinate
            end_x: Ending X coordinate
            end_y: Ending Y coordinate
            duration: Duration of drag in seconds
            
        Returns:
            Success status
        """
        if not self.gui_available:
            print("⚠️  GUI automation not available (PyAutoGUI not installed)")
            return False
            
        try:
            if not (self._validate_coordinates(start_x, start_y) and 
                    self._validate_coordinates(end_x, end_y)):
                return False
                
            pyautogui.drag(start_x, start_y, end_x - start_x, end_y - start_y, 
                          duration=duration)
            return True
        except Exception as e:
            print(f"Mouse drag failed: {e}")
            return False
    
    def get_mouse_position(self) -> Tuple[int, int]:
        """
        Get current mouse position.
        
        Returns:
            Tuple of (x, y) coordinates
        """
        if not self.gui_available:
            return (0, 0)  # Fallback
        return pyautogui.position()
    
    def wait(self, seconds: float) -> None:
        """
        Wait for specified number of seconds.
        
        Args:
            seconds: Number of seconds to wait
        """
        time.sleep(seconds)
    
    def _validate_coordinates(self, x: int, y: int) -> bool:
        """
        Validate that coordinates are within screen bounds.
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            True if coordinates are valid
        """
        return 0 <= x <= self.screen_width and 0 <= y <= self.screen_height
    
    def _is_dangerous_command(self, command: str) -> bool:
        """
        Check if a command is potentially dangerous.
        
        Args:
            command: Command to check
            
        Returns:
            True if command is dangerous
        """
        command_lower = command.lower()
        return any(dangerous in command_lower for dangerous in self.dangerous_commands)