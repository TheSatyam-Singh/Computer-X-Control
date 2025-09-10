# Computer-X-Control

🤖 **LLM-Powered PC Automation Tool**

Computer-X-Control is a powerful tool that allows Large Language Models (LLMs) to control your PC through natural language commands. Simply describe what you want to do, and the AI will translate your instructions into precise computer actions.

## ✨ Features

- 🧠 **Natural Language Control**: Control your PC using plain English commands
- 🔗 **Multiple LLM Support**: Works with OpenAI GPT and Anthropic Claude
- 🖱️ **GUI Automation**: Click, type, scroll, drag and drop
- ⌨️ **Keyboard Control**: Press any key or key combinations
- 📱 **Application Management**: Open and control applications
- 📸 **Screenshots**: Capture screen images for analysis
- 🖥️ **System Commands**: Execute system commands safely
- 🛡️ **Safety Mode**: Built-in protection against dangerous operations
- 🎯 **Multi-Action Support**: Execute complex sequences of actions

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/TheSatyam-Singh/Computer-X-Control.git
cd Computer-X-Control

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Copy the example environment file and add your API keys:

```bash
cp .env.example .env
```

Edit `.env` and add your LLM API key:

```bash
# For OpenAI
OPENAI_API_KEY=your_openai_api_key_here

# For Anthropic (optional)
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

### 3. Run the Tool

```bash
# Interactive mode
python main.py

# Single command
python main.py -c "take a screenshot"

# Use Anthropic Claude instead of OpenAI
python main.py --llm anthropic

# Execute commands from a file
python main.py -f commands.txt
```

## 💬 Example Commands

Here are some example natural language commands you can use:

### Basic Actions
- `"Take a screenshot"`
- `"Click at position 100, 200"`
- `"Type hello world"`
- `"Press the enter key"`
- `"Press ctrl+c to copy"`

### Application Control
- `"Open notepad"`
- `"Open calculator"`
- `"Open chrome browser"`

### Mouse Operations
- `"Move mouse to 300, 400"`
- `"Right click at 150, 250"`
- `"Double click in the center of screen"`
- `"Drag from 100,100 to 300,300"`

### Scrolling and Navigation
- `"Scroll down 5 times"`
- `"Scroll up"`
- `"Page down"`

### Complex Operations
- `"Open notepad, wait 2 seconds, then type 'Hello AI!'"`
- `"Take a screenshot, then click at 200,300"`

## 🏗️ Architecture

The tool consists of four main components:

### 1. PC Controller (`computer_x_control/automation/pc_controller.py`)
Handles all low-level PC automation:
- Mouse operations (click, move, drag)
- Keyboard input (typing, key presses)
- Screen capture
- Application launching
- System command execution

### 2. LLM Interface (`computer_x_control/llm/llm_interface.py`)
Manages communication with AI models:
- OpenAI GPT integration
- Anthropic Claude integration
- Natural language command parsing
- JSON response generation

### 3. Command Parser (`computer_x_control/parser/command_parser.py`)
Translates LLM responses into actions:
- Command validation
- Action execution
- Error handling
- Multi-action sequences

### 4. Main Application (`main.py`)
Provides the user interface:
- Interactive command mode
- Single command execution
- File-based command execution
- Configuration management

## 🛡️ Safety Features

- **Safety Mode**: Blocks potentially dangerous commands by default
- **Command Validation**: Validates all commands before execution
- **Coordinate Bounds**: Ensures mouse operations stay within screen bounds
- **Timeout Protection**: Prevents infinite command execution
- **Dangerous Command Detection**: Identifies and blocks risky system commands

## 📋 Available Actions

The LLM can generate the following action types:

| Action | Description | Example |
|--------|-------------|---------|
| `click` | Click at coordinates | `{"action": "click", "x": 100, "y": 200}` |
| `type` | Type text | `{"action": "type", "text": "hello"}` |
| `key` | Press keys | `{"action": "key", "key": "enter"}` |
| `scroll` | Scroll up/down | `{"action": "scroll", "direction": "up"}` |
| `screenshot` | Take screenshot | `{"action": "screenshot"}` |
| `open_app` | Open application | `{"action": "open_app", "app_name": "notepad"}` |
| `command` | Run system command | `{"action": "command", "command": "dir"}` |
| `move_mouse` | Move mouse | `{"action": "move_mouse", "x": 100, "y": 200}` |
| `drag` | Drag mouse | `{"action": "drag", "start_x": 100, "start_y": 100, "end_x": 200, "end_y": 200}` |
| `wait` | Wait seconds | `{"action": "wait", "seconds": 2.0}` |
| `multiple` | Multiple actions | `{"action": "multiple", "actions": [...]}` |

## ⚙️ Configuration Options

### Command Line Arguments

```bash
python main.py [OPTIONS]

Options:
  --llm {openai,anthropic}  LLM provider to use (default: openai)
  --no-safety              Disable safety mode (use with caution)
  -c, --command TEXT       Execute a single command
  -f, --file TEXT          Execute commands from a file
```

### Environment Variables

```bash
# Required (choose one)
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here

# Optional safety settings
ENABLE_SYSTEM_COMMANDS=true
ENABLE_FILE_OPERATIONS=true
ENABLE_WEB_AUTOMATION=true
```

## 📄 File-based Execution

Create a text file with commands (one per line):

```text
# commands.txt
take a screenshot
open notepad
wait 2 seconds
type Hello from Computer-X-Control!
press enter
```

Execute with:
```bash
python main.py -f commands.txt
```

## 🔧 Development

### Project Structure

```
Computer-X-Control/
├── computer_x_control/
│   ├── automation/          # PC control functionality
│   ├── llm/                # LLM integration
│   ├── parser/             # Command parsing
│   └── utils/              # Utility functions
├── main.py                 # Main application
├── requirements.txt        # Dependencies
├── .env.example           # Environment template
└── README.md              # Documentation
```

### Adding New Actions

1. Add the action to `PCController` class
2. Update the `LLMInterface` system prompt
3. Add execution method to `CommandParser`
4. Update the action map in `CommandParser.__init__`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## ⚠️ Disclaimer

This tool can control your computer and execute system commands. Use with caution:

- Always run in safety mode when possible
- Review commands before execution in production environments
- Test thoroughly in safe environments first
- Keep your API keys secure and private

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [PyAutoGUI](https://pyautogui.readthedocs.io/) for GUI automation
- [OpenAI](https://openai.com/) for GPT models
- [Anthropic](https://anthropic.com/) for Claude models