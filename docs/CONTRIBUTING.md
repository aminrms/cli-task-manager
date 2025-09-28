# 🤝 Contributing to CLI Task Manager

Thank you for your interest in contributing to CLI Task Manager! This document provides guidelines and information for contributors.

## 🌟 Ways to Contribute

- 🐛 **Bug Reports** - Help us identify and fix issues
- 💡 **Feature Requests** - Suggest new features and improvements
- 📝 **Code Contributions** - Submit bug fixes and new features
- 📖 **Documentation** - Improve documentation and examples
- 🌍 **Translations** - Add support for new languages
- 🎨 **UI/UX** - Improve the user interface and experience
- 🧪 **Testing** - Add tests and improve test coverage

## 🚀 Getting Started

### **Prerequisites**
- Python 3.8 or higher
- Git
- Familiarity with terminal/command line

### **Setup Development Environment**
```bash
# 1. Fork the repository on GitHub
# 2. Clone your fork
git clone https://github.com/YOUR_USERNAME/cli-task-manager.git
cd cli-task-manager

# 3. Set up upstream remote
git remote add upstream https://github.com/ORIGINAL_OWNER/cli-task-manager.git

# 4. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 5. Install development dependencies
pip install -r requirements-dev.txt

# 6. Install in development mode
pip install -e .

# 7. Run tests to verify setup
pytest
```

## 📋 Development Workflow

### **1. Create a Feature Branch**
```bash
# Update your main branch
git checkout main
git pull upstream main

# Create and switch to feature branch
git checkout -b feature/your-feature-name
```

### **2. Make Your Changes**
- Write code following our style guidelines
- Add tests for new functionality
- Update documentation as needed
- Ensure all tests pass

### **3. Test Your Changes**
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Check code style
flake8 src/ tests/

# Format code
black src/ tests/

# Type checking
mypy src/
```

### **4. Commit Your Changes**
```bash
# Stage your changes
git add .

# Commit with descriptive message
git commit -m "Add: Brief description of your changes"
```

### **5. Push and Create Pull Request**
```bash
# Push to your fork
git push origin feature/your-feature-name

# Go to GitHub and create a Pull Request
```

## 📝 Code Style Guidelines

### **Python Style**
- Follow **PEP 8** style guidelines
- Use **type hints** for function parameters and return values
- Write **docstrings** for all public functions and classes
- Keep lines under **88 characters** (Black formatter default)

### **Code Formatting**
```bash
# Format code with Black
black src/ tests/

# Sort imports with isort
isort src/ tests/

# Lint with flake8
flake8 src/ tests/
```

### **Example Code Style**
```python
from typing import List, Optional, Dict, Any
from rich.console import Console

def process_tasks(
    tasks: List[Dict[str, Any]], 
    filter_date: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Process and filter tasks based on criteria.
    
    Args:
        tasks: List of task dictionaries
        filter_date: Optional date string to filter by
        
    Returns:
        Filtered list of tasks
        
    Raises:
        ValueError: If date format is invalid
    """
    if not tasks:
        return []
    
    if filter_date:
        return [task for task in tasks if task.get("date") == filter_date]
    
    return tasks
```

## 🧪 Testing Guidelines

### **Writing Tests**
- Write tests for all new functionality
- Use **pytest** framework
- Aim for **high test coverage** (80%+)
- Test both **happy path** and **error cases**

### **Test Structure**
```python
import pytest
from src.core.task import Task

class TestTask:
    """Test suite for Task class."""
    
    def test_task_creation(self):
        """Test basic task creation."""
        task = Task(
            date="2023-12-01",
            duration="2h",
            task="Test task",
            description="Test description"
        )
        
        assert task.date == "2023-12-01"
        assert task.duration == "2h"
        assert task.task == "Test task"
    
    def test_task_validation_invalid_date(self):
        """Test task validation with invalid date."""
        with pytest.raises(ValueError):
            Task(
                date="invalid-date",
                duration="1h",
                task="Test task",
                description=""
            )
```

### **Running Tests**
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_core/test_task.py

# Run with coverage
pytest --cov=src --cov-report=html

# Run with verbose output
pytest -v
```

## 📖 Documentation Guidelines

### **Code Documentation**
- Write clear **docstrings** for all public APIs
- Use **Google style** docstrings
- Include **type hints** for parameters and return values
- Add **examples** in docstrings where helpful

### **README Updates**
- Update README.md for new features
- Add usage examples
- Update installation instructions if needed

### **Changelog**
- Add entries to CHANGELOG.md for all changes
- Follow [Keep a Changelog](https://keepachangelog.com/) format
- Include breaking changes, new features, bug fixes

## 🐛 Bug Reports

### **Before Submitting**
- Check if the bug has already been reported
- Test with the latest version
- Gather relevant information

### **Bug Report Template**
```markdown
**Bug Description**
A clear description of the bug.

**Steps to Reproduce**
1. Go to '...'
2. Click on '...'
3. Run command '...'
4. See error

**Expected Behavior**
What you expected to happen.

**Actual Behavior**
What actually happened.

**Environment**
- OS: [e.g., Windows 10, macOS 12, Ubuntu 20.04]
- Python Version: [e.g., 3.9.7]
- CLI Task Manager Version: [e.g., 2.0.0]

**Additional Context**
Any other context about the problem.
```

## 💡 Feature Requests

### **Feature Request Template**
```markdown
**Feature Description**
A clear description of the feature you'd like to see.

**Problem/Use Case**
What problem does this feature solve?

**Proposed Solution**
How do you think this should work?

**Alternatives Considered**
Any alternative solutions you've considered.

**Additional Context**
Any other context or screenshots about the feature.
```

## 🔍 Code Review Process

### **What We Look For**
- **Correctness** - Does the code work as intended?
- **Style** - Does it follow our style guidelines?
- **Tests** - Are there adequate tests?
- **Documentation** - Is it properly documented?
- **Performance** - Are there any performance concerns?

### **Review Checklist**
- [ ] Code follows style guidelines
- [ ] Tests are included and pass
- [ ] Documentation is updated
- [ ] No breaking changes (or properly documented)
- [ ] Performance impact considered
- [ ] Security implications reviewed

## 🏷️ Commit Message Guidelines

### **Format**
```
Type: Brief description

Longer description if needed.

Fixes #123
```

### **Types**
- **Add:** New feature or functionality
- **Fix:** Bug fix
- **Update:** Update existing functionality
- **Remove:** Remove functionality
- **Refactor:** Code refactoring
- **Docs:** Documentation changes
- **Test:** Add or update tests
- **Style:** Code style changes
- **Build:** Build system changes

### **Examples**
```bash
Add: Support for custom themes in UI components

Fix: Navigation menu not displaying all options on Windows

Update: Improve error handling in data manager

Docs: Add development setup guide for macOS

Test: Add unit tests for task validation
```

## 🌍 Translation Guidelines

### **Adding New Languages**
1. Create language file in `src/i18n/`
2. Translate all text strings
3. Update language selection in config
4. Add tests for new language
5. Update documentation

### **Translation Files**
```python
# src/i18n/en.py
MESSAGES = {
    "welcome": "Welcome to CLI Task Manager",
    "add_task": "Add New Task",
    "list_tasks": "List All Tasks",
    # ... more translations
}

# src/i18n/fa.py (Persian)
MESSAGES = {
    "welcome": "به مدیر وظایف خط فرمان خوش آمدید",
    "add_task": "افزودن وظیفه جدید",
    "list_tasks": "لیست همه وظایف",
    # ... more translations
}
```

## 🚀 Release Process

### **Version Numbering**
We follow [Semantic Versioning](https://semver.org/):
- **MAJOR.MINOR.PATCH** (e.g., 2.1.0)
- **Major** - Breaking changes
- **Minor** - New features (backward compatible)
- **Patch** - Bug fixes (backward compatible)

### **Release Checklist**
- [ ] All tests pass
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Version bumped in setup.py
- [ ] Git tag created
- [ ] PyPI package uploaded
- [ ] GitHub release created

## 🎯 Project Priorities

### **High Priority**
- Bug fixes and stability improvements
- Cross-platform compatibility
- Performance optimizations
- Security enhancements

### **Medium Priority**
- New features
- UI/UX improvements
- Additional language support
- Plugin system

### **Low Priority**
- Advanced features
- Experimental functionality
- Nice-to-have improvements

## 💬 Communication

### **Channels**
- **GitHub Issues** - Bug reports and feature requests
- **GitHub Discussions** - General discussion and questions
- **Pull Requests** - Code contributions and reviews
- **Email** - Direct contact for sensitive issues

### **Community Guidelines**
- Be respectful and inclusive
- Help others learn and grow
- Share knowledge and experience
- Follow our Code of Conduct

## 🏆 Recognition

Contributors will be:
- Listed in AUTHORS.md
- Mentioned in release notes
- Given credit in documentation
- Invited to join the core team (for significant contributors)

## 📞 Getting Help

- **Documentation** - Check existing docs first
- **GitHub Issues** - Search for similar issues
- **GitHub Discussions** - Ask questions and get help
- **Discord/Slack** - Real-time chat (if available)

## 📜 License

By contributing to CLI Task Manager, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to CLI Task Manager! 🚀**

Every contribution, no matter how small, makes a difference and helps improve the project for everyone.
