"""
Data Manager Module
Handles CSV file operations and data persistence
"""

import csv
import os
import shutil
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime

from rich.console import Console
from .task import Task
from .config import Config

console = Console()

class DataManager:
    """Handles data persistence and CSV operations"""
    
    def __init__(self, config: Config):
        self.config = config
        csv_path = Path(config.get_csv_file())
        
        # Fix if path points to directory instead of file
        if csv_path.is_dir() or not csv_path.suffix:
            csv_path = csv_path / "تایم های کاری.csv"
            # Update config with corrected path
            config.set("csv_file", str(csv_path))
        
        self.csv_file = csv_path
        self.backup_dir = self.csv_file.parent / "backups"
        self._ensure_data_files()
    
    def _ensure_data_files(self):
        """Ensure CSV file and backup directory exist"""
        # Create directory if it doesn't exist
        self.csv_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Create CSV file with headers if it doesn't exist
        if not self.csv_file.exists():
            self._create_csv_file()
        
        # Create backup directory
        if self.config.get("auto_backup", True):
            self.backup_dir.mkdir(exist_ok=True)
    
    def _create_csv_file(self):
        """Create CSV file with proper headers"""
        headers = [
            "date", "duration", "task", "description", 
            "status", "priority", "tags", "created_at", "updated_at"
        ]
        
        try:
            with open(self.csv_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(headers)
            console.print(f"[green]📋 Created tasks file: {self.csv_file}[/green]")
        except IOError as e:
            console.print(f"[red]❌ Error creating CSV file: {e}[/red]")
            raise
    
    def backup_data(self):
        """Create backup of current data"""
        if not self.config.get("auto_backup", True):
            return
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = self.backup_dir / f"tasks_backup_{timestamp}.csv"
            shutil.copy2(self.csv_file, backup_file)
            
            # Keep only recent backups
            self._cleanup_old_backups()
            
        except IOError as e:
            console.print(f"[yellow]⚠️ Backup failed: {e}[/yellow]")
    
    def _cleanup_old_backups(self):
        """Remove old backup files"""
        backup_count = self.config.get("backup_count", 5)
        backup_files = sorted(
            self.backup_dir.glob("tasks_backup_*.csv"),
            key=lambda x: x.stat().st_mtime,
            reverse=True
        )
        
        # Remove excess backups
        for backup_file in backup_files[backup_count:]:
            try:
                backup_file.unlink()
            except OSError:
                pass
    
    def load_tasks(self) -> List[Task]:
        """Load all tasks from CSV file"""
        tasks = []
        
        if not self.csv_file.exists():
            return tasks
        
        try:
            with open(self.csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for idx, row in enumerate(reader, 1):
                    try:
                        task = Task.from_csv_row(row, task_id=idx)
                        tasks.append(task)
                    except Exception as e:
                        console.print(f"[yellow]⚠️ Error loading task {idx}: {e}[/yellow]")
                        continue
        
        except IOError as e:
            console.print(f"[red]❌ Error reading tasks: {e}[/red]")
        
        return tasks
    
    def save_tasks(self, tasks: List[Task]):
        """Save all tasks to CSV file"""
        # Create backup before saving
        if self.csv_file.exists():
            self.backup_data()
        
        try:
            with open(self.csv_file, 'w', newline='', encoding='utf-8') as file:
                if not tasks:
                    # Write headers even if no tasks
                    writer = csv.writer(file)
                    writer.writerow([
                        "date", "duration", "task", "description", 
                        "status", "priority", "tags", "created_at", "updated_at"
                    ])
                else:
                    # Write tasks with proper headers
                    fieldnames = [
                        "date", "duration", "task", "description", 
                        "status", "priority", "tags", "created_at", "updated_at"
                    ]
                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                    writer.writeheader()
                    
                    for task in tasks:
                        row_data = task.to_csv_row()
                        # Add metadata fields
                        row_data.update({
                            'created_at': task.created_at or '',
                            'updated_at': task.updated_at or ''
                        })
                        writer.writerow(row_data)
        
        except IOError as e:
            console.print(f"[red]❌ Error saving tasks: {e}[/red]")
            raise
    
    def add_task(self, task: Task) -> bool:
        """Add a single task"""
        try:
            tasks = self.load_tasks()
            # Assign new ID
            task.id = len(tasks) + 1
            tasks.append(task)
            self.save_tasks(tasks)
            return True
        except Exception as e:
            console.print(f"[red]❌ Error adding task: {e}[/red]")
            return False
    
    def update_task(self, task_index: int, updated_task: Task) -> bool:
        """Update an existing task"""
        try:
            tasks = self.load_tasks()
            if 0 <= task_index < len(tasks):
                updated_task.id = tasks[task_index].id
                updated_task.created_at = tasks[task_index].created_at
                updated_task.updated_at = datetime.now().isoformat()
                tasks[task_index] = updated_task
                self.save_tasks(tasks)
                return True
            return False
        except Exception as e:
            console.print(f"[red]❌ Error updating task: {e}[/red]")
            return False
    
    def delete_task(self, task_index: int) -> bool:
        """Delete a task by index"""
        try:
            tasks = self.load_tasks()
            if 0 <= task_index < len(tasks):
                tasks.pop(task_index)
                # Reassign IDs
                for i, task in enumerate(tasks, 1):
                    task.id = i
                self.save_tasks(tasks)
                return True
            return False
        except Exception as e:
            console.print(f"[red]❌ Error deleting task: {e}[/red]")
            return False
    
    def clear_all_tasks(self) -> bool:
        """Delete all tasks"""
        try:
            self.save_tasks([])
            return True
        except Exception as e:
            console.print(f"[red]❌ Error clearing tasks: {e}[/red]")
            return False
    
    def search_tasks(self, query: str) -> List[Task]:
        """Search tasks by query"""
        tasks = self.load_tasks()
        return [task for task in tasks if task.matches_filter("search", query)]
    
    def filter_tasks(self, filter_type: str, filter_value: str) -> List[Task]:
        """Filter tasks by criteria"""
        tasks = self.load_tasks()
        return [task for task in tasks if task.matches_filter(filter_type, filter_value)]
    
    def get_today_tasks(self) -> List[Task]:
        """Get tasks for today"""
        date_format = self.config.get_date_format()
        tasks = self.load_tasks()
        return [task for task in tasks if task.is_today(date_format)]
    
    def get_task_count(self) -> int:
        """Get total number of tasks"""
        return len(self.load_tasks())
    
    def get_tasks_by_status(self, status: str) -> List[Task]:
        """Get tasks by status"""
        return self.filter_tasks("status", status)
    
    def get_tasks_by_priority(self, priority: str) -> List[Task]:
        """Get tasks by priority"""
        return self.filter_tasks("priority", priority)
    
    def export_data(self, export_path: str, format_type: str = "csv") -> bool:
        """Export data to different formats"""
        try:
            export_path = Path(export_path)
            tasks = self.load_tasks()
            
            if format_type.lower() == "csv":
                shutil.copy2(self.csv_file, export_path)
            elif format_type.lower() == "json":
                import json
                with open(export_path, 'w', encoding='utf-8') as f:
                    json.dump([task.to_dict() for task in tasks], f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            console.print(f"[red]❌ Export failed: {e}[/red]")
            return False
    
    def import_data(self, import_path: str) -> bool:
        """Import data from file"""
        try:
            import_path = Path(import_path)
            if not import_path.exists():
                console.print(f"[red]❌ Import file not found: {import_path}[/red]")
                return False
            
            # Create backup before import
            self.backup_data()
            
            if import_path.suffix.lower() == '.csv':
                shutil.copy2(import_path, self.csv_file)
            elif import_path.suffix.lower() == '.json':
                import json
                with open(import_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                tasks = [Task.from_dict(item) for item in data]
                self.save_tasks(tasks)
            
            return True
        except Exception as e:
            console.print(f"[red]❌ Import failed: {e}[/red]")
            return False
    
    def get_data_info(self) -> Dict[str, Any]:
        """Get information about data file"""
        info = {
            "csv_file": str(self.csv_file),
            "file_exists": self.csv_file.exists(),
            "file_size": 0,
            "task_count": 0,
            "last_modified": None,
            "backup_count": 0
        }
        
        if self.csv_file.exists():
            stat = self.csv_file.stat()
            info["file_size"] = stat.st_size
            info["last_modified"] = datetime.fromtimestamp(stat.st_mtime).isoformat()
            info["task_count"] = self.get_task_count()
        
        if self.backup_dir.exists():
            info["backup_count"] = len(list(self.backup_dir.glob("tasks_backup_*.csv")))
        
        return info
