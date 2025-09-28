# 🏗️ Development Guide

This guide will help you set up CLI Task Manager for development on any operating system.

## 🚀 Quick Development Setup

### **Prerequisites**
- **Python 3.8+** ([Download](https://www.python.org/downloads/))
- **Git** ([Download](https://git-scm.com/downloads))
- **Terminal/Command Prompt** access

### **One-Command Setup**
```bash
# Clone, setup, and run in one go
git clone https://github.com/yourusername/cli-task-manager.git && cd cli-task-manager && python -m venv venv && source venv/bin/activate && pip install -r requirements-dev.txt && python main.py
```

## 📋 Step-by-Step Setup

### **1. Clone the Repository**
```bash
git clone https://github.com/yourusername/cli-task-manager.git
cd cli-task-manager
```

### **2. Create Virtual Environment**

#### **Windows (Command Prompt/PowerShell)**
```cmd
python -m venv venv
venv\Scripts\activate
```

#### **Windows (Git Bash)**
```bash
python -m venv venv
source venv/Scripts/activate
```

#### **macOS/Linux**
```bash
python3 -m venv venv
source venv/bin/activate
```

### **3. Install Dependencies**
```bash
# Install development dependencies (includes production deps)
pip install -r requirements-dev.txt

# Or install in development mode
pip install -e .
```

### **4. Verify Installation**
```bash
# Run the application
python main.py

# Run tests
pytest

# Check code quality
flake8 src/
```

## 🏢 Platform-Specific Setup

### **🪟 Windows Development**

#### **Using Command Prompt**
```cmd
@echo off
REM Setup script for Windows Command Prompt
echo Setting up CLI Task Manager for development...

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python not found. Please install Python 3.8+
    exit /b 1
)

REM Clone and setup
git clone https://github.com/yourusername/cli-task-manager.git
cd cli-task-manager
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements-dev.txt

echo Setup complete! Run: python main.py
```

#### **Using PowerShell**
```powershell
# Setup script for PowerShell
Write-Host "Setting up CLI Task Manager for development..." -ForegroundColor Cyan

# Check Python
try {
    $pythonVersion = python --version
    Write-Host "✓ Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found. Please install Python 3.8+" -ForegroundColor Red
    exit 1
}

# Clone and setup
git clone https://github.com/yourusername/cli-task-manager.git
Set-Location cli-task-manager
python -m venv venv
& "venv\Scripts\Activate.ps1"
pip install -r requirements-dev.txt

Write-Host "Setup complete! Run: python main.py" -ForegroundColor Green
```

### **🍎 macOS Development**

#### **Using Homebrew (Recommended)**
```bash
#!/bin/bash
# Setup script for macOS

echo "🚀 Setting up CLI Task Manager for development..."

# Install Python via Homebrew if not present
if ! command -v python3 &> /dev/null; then
    echo "Installing Python via Homebrew..."
    brew install python
fi

# Clone and setup
git clone https://github.com/yourusername/cli-task-manager.git
cd cli-task-manager
python3 -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt

echo "✅ Setup complete! Run: python main.py"
```

#### **Manual Setup**
```bash
# Check if Python 3.8+ is installed
python3 --version

# If not, install via official installer or Homebrew
# Homebrew: brew install python
# Official: https://www.python.org/downloads/

# Clone and setup
git clone https://github.com/yourusername/cli-task-manager.git
cd cli-task-manager
python3 -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt
```

### **🐧 Linux Development**

#### **Ubuntu/Debian**
```bash
#!/bin/bash
# Setup script for Ubuntu/Debian

echo "🚀 Setting up CLI Task Manager for development..."

# Install Python and pip if not present
sudo apt update
sudo apt install -y python3 python3-pip python3-venv git

# Clone and setup
git clone https://github.com/yourusername/cli-task-manager.git
cd cli-task-manager
python3 -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt

echo "✅ Setup complete! Run: python main.py"
```

#### **CentOS/RHEL/Fedora**
```bash
#!/bin/bash
# Setup script for CentOS/RHEL/Fedora

echo "🚀 Setting up CLI Task Manager for development..."

# Install Python and pip (adjust for your distro)
# CentOS/RHEL: sudo yum install -y python3 python3-pip git
# Fedora: sudo dnf install -y python3 python3-pip git

# Clone and setup
git clone https://github.com/yourusername/cli-task-manager.git
cd cli-task-manager
python3 -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt

echo "✅ Setup complete! Run: python main.py"
```

#### **Arch Linux**
```bash
#!/bin/bash
# Setup script for Arch Linux

echo "🚀 Setting up CLI Task Manager for development..."

# Install Python and pip
sudo pacman -S python python-pip git

# Clone and setup
git clone https://github.com/yourusername/cli-task-manager.git
cd cli-task-manager
python -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt

echo "✅ Setup complete! Run: python main.py"
```

## 🛠️ Development Tools

### **Code Quality Tools**
```bash
# Install quality tools
pip install black flake8 mypy pytest-cov pre-commit

# Format code
black src/ tests/

# Check code style
flake8 src/ tests/

# Type checking
mypy src/

# Run tests with coverage
pytest --cov=src --cov-report=html
```

### **Pre-commit Hooks**
```bash
# Install pre-commit hooks
pre-commit install

# Run pre-commit on all files
pre-commit run --all-files
```

### **Development Scripts**
Create these helpful scripts in your development environment:

#### **`dev.py` - Development Helper**
```python
#!/usr/bin/env python3
"""Development helper script"""
import subprocess
import sys
import os

def run_tests():
    """Run all tests"""
    return subprocess.run([sys.executable, "-m", "pytest", "-v"])

def run_quality():
    """Run code quality checks"""
    subprocess.run([sys.executable, "-m", "black", "src/", "tests/"])
    subprocess.run([sys.executable, "-m", "flake8", "src/", "tests/"])
    subprocess.run([sys.executable, "-m", "mypy", "src/"])

def run_app():
    """Run the application"""
    subprocess.run([sys.executable, "main.py"])

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "test":
            run_tests()
        elif sys.argv[1] == "quality":
            run_quality()
        elif sys.argv[1] == "run":
            run_app()
        else:
            print("Usage: python dev.py [test|quality|run]")
    else:
        run_app()
```

## 🧪 Testing

### **Running Tests**
```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_core/test_task.py

# Run with coverage
pytest --cov=src

# Generate HTML coverage report
pytest --cov=src --cov-report=html
```

### **Test Structure**
```
tests/
├── __init__.py
├── conftest.py              # Pytest configuration
├── test_core/
│   ├── test_config.py
│   ├── test_task.py
│   └── test_data_manager.py
├── test_ui/
│   ├── test_display.py
│   └── test_input_handler.py
└── test_utils/
    └── test_navigation.py
```

## 🔧 Configuration for Development

### **Environment Variables**
```bash
# Set development environment
export CLI_TASK_ENV=development
export CLI_TASK_DEBUG=true
export CLI_TASK_LOG_LEVEL=DEBUG

# Or create .env file
echo "CLI_TASK_ENV=development" > .env
echo "CLI_TASK_DEBUG=true" >> .env
echo "CLI_TASK_LOG_LEVEL=DEBUG" >> .env
```

### **Development Configuration**
```json
{
  "csv_file": "./dev_tasks.csv",
  "date_format": "gregorian",
  "default_duration": "30min",
  "backup_enabled": false,
  "debug_mode": true,
  "log_level": "DEBUG"
}
```

## 🚀 Building and Distribution

### **Building Package**
```bash
# Install build tools
pip install build twine

# Build package
python -m build

# Check package
twine check dist/*

# Upload to PyPI (test)
twine upload --repository testpypi dist/*

# Upload to PyPI (production)
twine upload dist/*
```

### **Creating Executables**
```bash
# Install PyInstaller
pip install pyinstaller

# Create executable
pyinstaller --onefile --name=mytasks main.py

# Create with icon (Windows)
pyinstaller --onefile --icon=icon.ico --name=mytasks main.py
```

## 🐳 Docker Development

### **Dockerfile**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]
```

### **Docker Compose**
```yaml
version: '3.8'
services:
  cli-task-manager:
    build: .
    volumes:
      - .:/app
      - ~/.task-cli:/root/.task-cli
    stdin_open: true
    tty: true
```

## 🔍 Debugging

### **VS Code Setup**
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Main",
      "type": "python",
      "request": "launch",
      "program": "main.py",
      "console": "integratedTerminal",
      "cwd": "${workspaceFolder}"
    },
    {
      "name": "Python: Tests",
      "type": "python",
      "request": "launch",
      "module": "pytest",
      "args": ["-v"],
      "console": "integratedTerminal",
      "cwd": "${workspaceFolder}"
    }
  ]
}
```

### **PyCharm Setup**
1. Open the project directory
2. Configure Python interpreter to use the virtual environment
3. Set run configuration to execute `main.py`
4. Enable pytest as test runner

## 📝 Common Issues

### **Permission Issues (Windows)**
```cmd
# Run as Administrator if needed
# Or use specific Python path
C:\Users\Username\AppData\Local\Programs\Python\Python39\python.exe main.py
```

### **Module Not Found**
```bash
# Ensure virtual environment is activated
# Windows: venv\Scripts\activate
# Unix: source venv/bin/activate

# Install in development mode
pip install -e .
```

### **Terminal Encoding Issues**
```bash
# Set UTF-8 encoding
export PYTHONIOENCODING=utf-8

# Windows Command Prompt
chcp 65001
```

## 🤝 Contributing Workflow

1. **Fork** the repository
2. **Clone** your fork
3. **Create** a feature branch
4. **Make** your changes
5. **Test** your changes
6. **Commit** with good messages
7. **Push** to your fork
8. **Create** a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## 🎯 Development Best Practices

- **Follow PEP 8** style guidelines
- **Write tests** for new features
- **Document** your code
- **Use type hints** where appropriate
- **Keep commits** focused and atomic
- **Update documentation** for changes
- **Test on multiple platforms** when possible

---

**Happy coding! 🚀**
