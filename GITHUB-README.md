# 🚀 CLI Task Manager

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Cross Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)]()
[![Rich CLI](https://img.shields.io/badge/Rich-Terminal%20UI-brightgreen)](https://github.com/Textualize/rich)

A **beautiful, cross-platform terminal-based task manager** with Persian/Jalali date support, rich UI components, and professional modular architecture.

![CLI Task Manager Demo](docs/images/demo.gif)

## ✨ Features

### **Core Features**
- 🎨 **Beautiful Terminal UI** - Rich colors, tables, and interactive prompts
- 🎯 **Arrow Key Navigation** - Interactive menus with ↑↓ navigation and Enter selection
- 📅 **Jalali & Gregorian Dates** - Full Persian calendar integration with fallback
- 🌍 **Cross-Platform** - Works on Windows, macOS, and Linux
- 💾 **Configurable Storage** - Choose where to store your tasks
- 🛡️ **Error Handling** - Robust error handling and user-friendly messages
- ⚡ **Easy Setup** - One-command installation for development

### **Advanced Features**
- **💫 Dynamic** - Runtime configuration and adaptive UI
- **⚙️ Configurable** - First-time setup wizard and persistent settings
- **📖 Readable** - Clean, documented modular code
- **🔧 Maintainable** - Separation of concerns and extensible design
- **🔄 Flexible** - Plugin-ready architecture and multiple data formats
- **📦 Modular** - Small, focused modules with single responsibilities

## 🚀 Quick Start

### **For Users**
```bash
# Clone the repository
git clone https://github.com/yourusername/cli-task-manager.git
cd cli-task-manager

# Install and run
pip install -r requirements.txt
python main.py
```

### **For Developers**
```bash
# Clone the repository
git clone https://github.com/yourusername/cli-task-manager.git
cd cli-task-manager

# Set up development environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements-dev.txt

# Run in development mode
python main.py
```

## 📁 Project Structure

```
cli-task-manager/
├── main.py                    # Main entry point
├── mytasks.py                 # Legacy standalone version
├── requirements.txt           # Production dependencies
├── requirements-dev.txt       # Development dependencies
├── setup.py                   # Package setup
├── src/                       # Source code modules
│   ├── __init__.py
│   ├── app.py                 # Main application controller
│   ├── core/                  # Core business logic
│   │   ├── __init__.py
│   │   ├── config.py          # Configuration management
│   │   ├── task.py            # Task data model
│   │   └── data_manager.py    # Data persistence
│   ├── ui/                    # User interface components
│   │   ├── __init__.py
│   │   ├── display.py         # UI display components
│   │   └── input_handler.py   # Input handling
│   └── utils/                 # Utility modules
│       ├── __init__.py
│       └── navigation.py      # Navigation utilities
├── scripts/                   # Platform-specific scripts
│   ├── install.sh             # Linux/macOS installer
│   ├── install.bat            # Windows installer
│   └── mytasks.ps1            # PowerShell script
├── tests/                     # Test suite
│   ├── __init__.py
│   ├── test_core/
│   ├── test_ui/
│   └── test_utils/
├── docs/                      # Documentation
│   ├── CONTRIBUTING.md
│   ├── DEVELOPMENT.md
│   ├── API.md
│   └── images/
└── examples/                  # Example configurations
    ├── sample_config.json
    └── sample_tasks.csv
```

## 🛠️ Installation

### **Method 1: pip install (Recommended)**
```bash
pip install cli-task-manager
mytasks
```

### **Method 2: From Source**
```bash
git clone https://github.com/yourusername/cli-task-manager.git
cd cli-task-manager
pip install -e .
mytasks
```

### **Method 3: Development Setup**
See [DEVELOPMENT.md](docs/DEVELOPMENT.md) for detailed development setup instructions.

## 📖 Usage

### **Starting the Application**
```bash
# After installation
mytasks

# Or run directly
python main.py
```

### **First Run**
1. **Welcome Screen** - Shows feature overview
2. **Setup Wizard** - Configure CSV location, date format, defaults
3. **Main Menu** - Beautiful arrow key navigation
4. **Ready to Use** - All features available

### **Menu Navigation**
- **↑↓** - Navigate through options
- **Enter** - Select highlighted option
- **Q** - Quick quit
- **1-9** - Quick select by number
- **Ctrl+C** - Exit anytime

### **Features**
- 🆕 **Add New Task** - Create tasks with date, duration, status, priority, tags
- 📋 **List All Tasks** - View tasks in beautiful tables
- ✏️ **Edit Task** - Modify existing tasks
- 🗑️ **Delete Task** - Remove specific tasks
- 🔍 **Filter/Search** - Advanced filtering and search
- 📅 **Today's Tasks** - Quick view of current day
- 📊 **Statistics** - Task analytics and insights
- ⚙️ **Configuration** - Customize settings
- 💾 **Import/Export** - Backup and restore data

## 🏗️ Development

### **Prerequisites**
- Python 3.8 or higher
- Git
- Terminal/Command Prompt

### **Development Setup**
```bash
# 1. Fork and clone the repository
git clone https://github.com/yourusername/cli-task-manager.git
cd cli-task-manager

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 4. Install development dependencies
pip install -r requirements-dev.txt

# 5. Install in development mode
pip install -e .

# 6. Run tests
pytest

# 7. Run the application
python main.py
```

### **Code Quality**
```bash
# Format code
black src/ tests/

# Lint code
flake8 src/ tests/

# Type checking
mypy src/

# Run all quality checks
make quality
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/test_core/test_task.py

# Run with verbose output
pytest -v
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](docs/CONTRIBUTING.md) for details.

### **Quick Contribution Steps**
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for your changes
5. Ensure all tests pass (`pytest`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## 📋 Roadmap

- [ ] **Plugin System** - Support for custom extensions
- [ ] **Theme System** - Multiple UI themes
- [ ] **Cloud Sync** - Sync tasks across devices
- [ ] **API Integration** - Connect with popular task services
- [ ] **Mobile Companion** - Mobile app integration
- [ ] **Team Collaboration** - Shared task management
- [ ] **Advanced Analytics** - Productivity insights
- [ ] **AI Integration** - Smart task suggestions

## 🔧 Configuration

The application supports extensive configuration:

```json
{
  "csv_file": "~/.task-cli/tasks.csv",
  "date_format": "jalali",
  "default_duration": "1h",
  "backup_enabled": true,
  "backup_count": 5,
  "theme": "default"
}
```

See [Configuration Guide](docs/configuration.md) for full details.

## 🌍 Internationalization

- **English** - Full support
- **Persian/Farsi** - Full support with Jalali calendar
- **More languages** - Coming soon (contributions welcome!)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Rich](https://github.com/Textualize/rich) - For beautiful terminal UI
- [jdatetime](https://github.com/pylover/jdatetime) - For Jalali date support
- Contributors and community members

## 📞 Support

- 📖 **Documentation**: [docs/](docs/)
- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/yourusername/cli-task-manager/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/yourusername/cli-task-manager/discussions)
- 📧 **Email**: support@cli-task-manager.com

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/cli-task-manager&type=Date)](https://star-history.com/#yourusername/cli-task-manager&Date)

---

**Made with ❤️ by the CLI Task Manager team**
