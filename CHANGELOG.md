# Changelog

All notable changes to CLI Task Manager will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- GitHub repository setup with comprehensive documentation
- Cross-platform installation scripts
- Development environment setup guide
- Contributing guidelines
- Package setup for PyPI distribution

### Changed
- Improved project structure for open source development
- Enhanced README with detailed setup instructions

## [2.0.0] - 2024-12-XX

### Added
- **Modular Architecture**: Complete refactoring into focused modules
- **Configuration System**: First-time setup wizard and persistent settings
- **Enhanced Task Model**: Added status, priority, and tags support
- **Data Management**: Automatic backups and import/export functionality
- **Beautiful UI Components**: Rich-based display with consistent styling
- **Navigation System**: Arrow key navigation with cross-platform support
- **Statistics**: Task analytics and productivity insights
- **Help System**: Comprehensive in-app help and guide

### Changed
- **Duration instead of Time**: Changed from specific time to duration tracking
- **Default Status**: Tasks now default to "completed" status
- **File Structure**: Organized code into `src/core/`, `src/ui/`, `src/utils/` modules
- **Configuration**: Settings stored in `~/.task-cli/config.json`
- **Navigation**: Improved menu system with better visibility

### Fixed
- **Cross-platform Compatibility**: Fixed Windows PowerShell support
- **Terminal Scrolling**: Resolved navigation menu visibility issues
- **Path Handling**: Better handling of CSV file paths and permissions
- **Screen Clearing**: Fixed navigation artifacts and display issues

### Technical
- **Type Hints**: Added comprehensive type annotations
- **Documentation**: Extensive docstrings and code documentation
- **Error Handling**: Improved error handling and user feedback
- **Testing**: Basic test structure prepared
- **Code Quality**: Consistent formatting and style

## [1.0.0] - 2024-11-XX

### Added
- **Initial Release**: Basic task management functionality
- **Jalali Date Support**: Persian calendar integration with jdatetime
- **Rich UI**: Beautiful terminal interface using Rich library
- **CSV Storage**: Task persistence in CSV format
- **Arrow Key Navigation**: Interactive menu system
- **CRUD Operations**: Create, read, update, delete tasks
- **Filtering**: Filter tasks by date and search functionality
- **Cross-platform**: Support for Windows, macOS, and Linux

### Features
- Add new tasks with date, time, name, and description
- List all tasks in a formatted table
- Edit existing tasks
- Delete specific tasks
- Filter tasks by date
- Search in task names and descriptions
- View today's tasks
- Clear all tasks with confirmation
- Help and usage guide

### Technical
- Python 3.8+ support
- Rich library for terminal UI
- jdatetime for Jalali calendar
- CSV file storage
- Cross-platform keyboard input handling
- Batch file for global Windows access
