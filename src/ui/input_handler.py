"""
Input Handler Module
Handles user input and form interactions
"""

import jdatetime
from datetime import datetime
from typing import Optional, List, Dict, Any
from rich.console import Console
from rich.prompt import Prompt, Confirm, IntPrompt
from rich.panel import Panel

from ..core.task import Task
from ..core.config import Config

console = Console()

class InputHandler:
    """Handles user input operations"""
    
    def __init__(self, config: Config):
        self.config = config
    
    def get_task_input(self, default_task: Optional[Task] = None) -> Optional[Task]:
        """Get task input from user"""
        console.rule("[bold green]📝 Task Input[/bold green]")
        
        try:
            # Get current date as default
            if self.config.get_date_format() == "jalali":
                current_date = jdatetime.date.today().isoformat()
            else:
                current_date = datetime.now().date().isoformat()
            
            # Get task details
            date = Prompt.ask(
                f"📅 Enter date ({self.config.get_date_format()} format YYYY-MM-DD)",
                default=default_task.date if default_task else current_date
            )
            
            duration = Prompt.ask(
                "⏱️ Enter duration (e.g., 2h, 30min, 1h 30min)",
                default=default_task.duration if default_task else self.config.get_default_duration()
            )
            
            task_name = Prompt.ask(
                "📝 Enter task name",
                default=default_task.task if default_task else ""
            )
            
            description = Prompt.ask(
                "📖 Enter description",
                default=default_task.description if default_task else ""
            )
            
            # Get optional fields
            status = Prompt.ask(
                "🏷️ Enter status",
                choices=["pending", "in_progress", "completed", "cancelled"],
                default=default_task.status if default_task else "completed"
            )
            
            priority = Prompt.ask(
                "⚡ Enter priority",
                choices=["low", "normal", "high", "critical"],
                default=default_task.priority if default_task else "normal"
            )
            
            # Get tags
            tags_input = Prompt.ask(
                "🏷️ Enter tags (comma-separated)",
                default=",".join(default_task.tags) if default_task and default_task.tags else ""
            )
            
            tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()]
            
            # Validate date
            if self.config.get_date_format() == "jalali":
                try:
                    jdate = jdatetime.date.fromisoformat(date)
                    date = jdate.isoformat()
                except ValueError:
                    console.print("[red]❌ Invalid Jalali date format![/red]")
                    return None
            
            # Create task
            task = Task(
                date=date,
                duration=duration,
                task=task_name,
                description=description,
                status=status,
                priority=priority,
                tags=tags
            )
            
            # Show preview and confirm
            return self._confirm_task(task)
            
        except KeyboardInterrupt:
            console.print("[yellow]❌ Input cancelled.[/yellow]")
            return None
        except Exception as e:
            console.print(f"[red]❌ Error getting input: {e}[/red]")
            return None
    
    def _confirm_task(self, task: Task) -> Optional[Task]:
        """Show task preview and get confirmation"""
        console.print()
        console.print(Panel(
            f"[cyan]📅 Date:[/cyan] {task.get_display_date()}\n"
            f"[yellow]⏱️ Duration:[/yellow] {task.duration}\n"
            f"[green]📝 Task:[/green] {task.task}\n"
            f"[white]📖 Description:[/white] {task.description}\n"
            f"[blue]🏷️ Status:[/blue] {task.status}\n"
            f"[magenta]⚡ Priority:[/magenta] {task.priority}\n"
            f"[cyan]🏷️ Tags:[/cyan] {', '.join(task.tags) if task.tags else 'None'}",
            title="Task Preview",
            style="blue"
        ))
        
        if Confirm.ask("💾 Save this task?", default=True):
            return task
        
        return None
    
    def get_search_query(self) -> Optional[str]:
        """Get search query from user"""
        try:
            query = Prompt.ask("🔍 Enter search term")
            return query.strip() if query.strip() else None
        except KeyboardInterrupt:
            return None
    
    def get_filter_date(self) -> Optional[str]:
        """Get date for filtering"""
        try:
            if self.config.get_date_format() == "jalali":
                default_date = jdatetime.date.today().isoformat()
            else:
                default_date = datetime.now().date().isoformat()
            
            date = Prompt.ask(
                f"📅 Enter date to filter ({self.config.get_date_format()} YYYY-MM-DD)",
                default=default_date
            )
            
            # Validate date
            if self.config.get_date_format() == "jalali":
                try:
                    jdate = jdatetime.date.fromisoformat(date)
                    return jdate.isoformat()
                except ValueError:
                    console.print("[red]❌ Invalid date format![/red]")
                    return None
            
            return date
            
        except KeyboardInterrupt:
            return None
    
    def get_export_path(self) -> Optional[str]:
        """Get export file path"""
        try:
            path = Prompt.ask("📁 Enter export file path")
            return path.strip() if path.strip() else None
        except KeyboardInterrupt:
            return None
    
    def get_import_path(self) -> Optional[str]:
        """Get import file path"""
        try:
            path = Prompt.ask("📁 Enter import file path")
            return path.strip() if path.strip() else None
        except KeyboardInterrupt:
            return None
    
    def get_config_update(self, current_config: Dict[str, Any]) -> Dict[str, Any]:
        """Get configuration updates from user"""
        console.rule("[bold blue]⚙️ Configuration Update[/bold blue]")
        
        updated_config = current_config.copy()
        
        try:
            # CSV file location
            csv_file = Prompt.ask(
                "📁 CSV file path",
                default=current_config.get("csv_file", "")
            )
            if csv_file.strip():
                updated_config["csv_file"] = csv_file.strip()
            
            # Date format
            date_format = Prompt.ask(
                "📅 Date format",
                choices=["jalali", "gregorian"],
                default=current_config.get("date_format", "jalali")
            )
            updated_config["date_format"] = date_format
            
            # Default duration
            default_duration = Prompt.ask(
                "⏱️ Default duration",
                default=current_config.get("default_duration", "1h")
            )
            updated_config["default_duration"] = default_duration
            
            # Auto backup
            auto_backup = Confirm.ask(
                "💾 Enable auto backup?",
                default=current_config.get("auto_backup", True)
            )
            updated_config["auto_backup"] = auto_backup
            
            # Backup count
            if auto_backup:
                backup_count = IntPrompt.ask(
                    "📦 Number of backups to keep",
                    default=current_config.get("backup_count", 5)
                )
                updated_config["backup_count"] = backup_count
            
            return updated_config
            
        except KeyboardInterrupt:
            console.print("[yellow]❌ Configuration update cancelled.[/yellow]")
            return current_config
    
    def confirm_action(self, message: str, default: bool = True) -> bool:
        """Get confirmation for an action"""
        try:
            return Confirm.ask(message, default=default)
        except KeyboardInterrupt:
            return False
    
    def get_selection(self, prompt: str, choices: List[str], default: str = None) -> Optional[str]:
        """Get selection from choices"""
        try:
            return Prompt.ask(prompt, choices=choices, default=default)
        except KeyboardInterrupt:
            return None
    
    def get_number_input(self, prompt: str, min_val: int = 1, max_val: int = None) -> Optional[int]:
        """Get number input with validation"""
        try:
            while True:
                try:
                    num = IntPrompt.ask(prompt)
                    if num < min_val:
                        console.print(f"[red]❌ Number must be at least {min_val}[/red]")
                        continue
                    if max_val and num > max_val:
                        console.print(f"[red]❌ Number must be at most {max_val}[/red]")
                        continue
                    return num
                except ValueError:
                    console.print("[red]❌ Please enter a valid number[/red]")
        except KeyboardInterrupt:
            return None
    
    def get_text_input(self, prompt: str, default: str = None, required: bool = False) -> Optional[str]:
        """Get text input with validation"""
        try:
            while True:
                text = Prompt.ask(prompt, default=default)
                if required and not text.strip():
                    console.print("[red]❌ This field is required[/red]")
                    continue
                return text.strip() if text else None
        except KeyboardInterrupt:
            return None
    
    def get_multiline_input(self, prompt: str) -> Optional[str]:
        """Get multiline text input"""
        console.print(f"{prompt} (Press Ctrl+D to finish, Ctrl+C to cancel)")
        lines = []
        try:
            while True:
                try:
                    line = input()
                    lines.append(line)
                except EOFError:
                    break
            return '\n'.join(lines) if lines else None
        except KeyboardInterrupt:
            return None
