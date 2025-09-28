#!/usr/bin/env python3
"""
Setup script for CLI Task Manager
"""

from setuptools import setup, find_packages
import os

# Read README for long description
def read_readme():
    """Read README file for long description."""
    try:
        with open("README.md", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "A beautiful, cross-platform terminal-based task manager"

# Read requirements
def read_requirements():
    """Read requirements from file."""
    try:
        with open("requirements.txt", "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip() and not line.startswith("#")]
    except FileNotFoundError:
        return ["rich>=12.0.0", "jdatetime>=4.1.0"]

# Read version from src/__init__.py
def get_version():
    """Get version from source code."""
    try:
        with open("src/__init__.py", "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("__version__"):
                    return line.split("=")[1].strip().strip('"\'')
    except FileNotFoundError:
        pass
    return "2.0.0"

setup(
    name="cli-task-manager",
    version=get_version(),
    author="CLI Task Manager Team",
    author_email="team@cli-task-manager.com",
    description="A beautiful, cross-platform terminal-based task manager",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/cli-task-manager",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/cli-task-manager/issues",
        "Source": "https://github.com/yourusername/cli-task-manager",
        "Documentation": "https://github.com/yourusername/cli-task-manager/docs",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Office/Business :: Scheduling",
        "Topic :: Utilities",
        "Environment :: Console",
        "Natural Language :: English",
        "Natural Language :: Persian",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=0.900",
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
            "pre-commit>=2.15.0",
        ],
        "docs": [
            "sphinx>=4.0.0",
            "sphinx-rtd-theme>=1.0.0",
        ],
        "build": [
            "build>=0.7.0",
            "twine>=3.8.0",
            "pyinstaller>=4.10",
        ],
    },
    entry_points={
        "console_scripts": [
            "mytasks=src.app:main",
            "cli-task-manager=src.app:main",
            "task-cli=src.app:main",
        ],
    },
    include_package_data=True,
    package_data={
        "src": ["*.json", "*.csv"],
        "": ["*.md", "*.txt", "*.yml", "*.yaml"],
    },
    keywords=[
        "task-manager",
        "cli",
        "terminal",
        "productivity",
        "todo",
        "tasks",
        "jalali",
        "persian",
        "rich",
        "tui",
    ],
    zip_safe=False,
)
