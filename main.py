#!/usr/bin/env python3
"""
Task CLI Manager - Main Entry Point
A beautiful, configurable task management CLI application

Features:
- Dynamic and configurable settings
- Modular architecture for maintainability  
- Beautiful terminal UI with arrow key navigation
- Jalali and Gregorian date support
- Automatic backups and data safety
- Import/Export functionality
- Powerful filtering and search
"""

import sys
import os
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def main():
    """Main application entry point"""
    try:
        from src.app import TaskManager
        
        # Create and run the application
        app = TaskManager()
        app.run()
        
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
        sys.exit(0)
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure all required packages are installed:")
        print("pip install rich jdatetime")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
