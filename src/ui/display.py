"""
UI Display Module
Handles all user interface display components
"""

import os
from typing import List, Optional, Dict, Any
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich.tree import Tree
from rich.columns import Columns

from ..core.task import Task
from ..core.config import Config

console = Console()

class UIManager:
    """Manages all UI display components"""
    
    def __init__(self, config: Optional[Config] = None):
        self.config = config
        self.console = console
    
    def show_header(self):
        """Display beautiful application header"""
        title_text = Text("🚀 Task CLI Manager", style="bold cyan")
        subtitle_text = Text("Manage your tasks beautifully", style="italic white")
        
        header_panel = Panel(
            Align.center(f"{title_text}\n{subtitle_text}"),
            style="cyan",
            title="Welcome",
            title_align="center"
        )
        console.print(header_panel)
        console.print()
    
    def show_tasks_table(self, tasks: List[Task], title: str = "📋 Your Task Schedule") -> None:
        """Display tasks in a beautiful table"""
        if not tasks:
            console.print(Panel(
                "[yellow]No tasks found! Use 'add' to create your first task.[/yellow]",
                title=title,
                style="yellow"
            ))
            return
        
        table = Table(
            title=f"{title} ({len(tasks)} tasks)",
            show_lines=True,
            title_style="bold cyan"
        )
        
        # Add columns
        table.add_column("#", style="dim", width=3)
        table.add_column("📅 Date", style="cyan", no_wrap=True, width=12)
        table.add_column("⏱️ Duration", style="yellow", width=10)
        table.add_column("📝 Task", style="green", min_width=15)
        table.add_column("📖 Description", style="white", min_width=20)
        table.add_column("🏷️ Status", style="blue", width=10)
        table.add_column("⚡ Priority", style="magenta", width=8)
        
        # Add rows
        for i, task in enumerate(tasks, 1):
            # Format status with colors
            status_style = {
                "pending": "[yellow]pending[/yellow]",
                "in_progress": "[blue]in progress[/blue]",
                "completed": "[green]completed[/green]",
                "cancelled": "[red]cancelled[/red]"
            }.get(task.status, task.status)
            
            # Format priority with colors
            priority_style = {
                "low": "[dim]low[/dim]",
                "normal": "[white]normal[/white]",
                "high": "[yellow]high[/yellow]",
                "critical": "[red]critical[/red]"
            }.get(task.priority, task.priority)
            
            table.add_row(
                str(i),
                task.get_display_date(self.config.get_date_format() if self.config else "jalali"),
                task.get_display_duration(),
                task.task,
                task.description,
                status_style,
                priority_style
            )
        
        console.print(table)
        
        # Calculate and show total duration
        total_hours = sum(task.get_duration_in_hours() for task in tasks)
        console.print(f"[bold green]⏱️ Total Duration: {total_hours} hours[/bold green]")
        console.print(f"[dim]Total tasks: {len(tasks)}[/dim]")
    
    def show_task_details(self, task: Task, title: str = "Task Details"):
        """Display detailed view of a single task"""
        details = f"[cyan]📅 Date:[/cyan] {task.get_display_date()}\n"
        details += f"[yellow]⏱️ Duration:[/yellow] {task.get_display_duration()}\n"
        details += f"[green]📝 Task:[/green] {task.task}\n"
        details += f"[white]📖 Description:[/white] {task.description}\n"
        details += f"[blue]🏷️ Status:[/blue] {task.status}\n"
        details += f"[magenta]⚡ Priority:[/magenta] {task.priority}"
        
        if task.tags:
            details += f"\n[cyan]🏷️ Tags:[/cyan] {', '.join(task.tags)}"
        
        if task.created_at:
            details += f"\n[dim]Created:[/dim] {task.created_at}"
        
        if task.updated_at:
            details += f"\n[dim]Updated:[/dim] {task.updated_at}"
        
        console.print(Panel(details, title=title, style="blue"))
    
    def show_menu_tree(self, menu_items: Dict[str, List[Dict[str, str]]]):
        """Display menu options in a tree structure"""
        menu_tree = Tree("📋 [bold cyan]Available Commands[/bold cyan]")
        
        for category, items in menu_items.items():
            category_branch = menu_tree.add(f"[yellow]{category}[/yellow]")
            for item in items:
                category_branch.add(f"[{item.get('color', 'white')}]{item['key']}[/{item.get('color', 'white')}] - {item['display']}")
        
        console.print(menu_tree)
    
    def show_statistics(self, stats: Dict[str, Any]):
        """Display task statistics"""
        stats_text = ""
        for key, value in stats.items():
            stats_text += f"[cyan]{key.replace('_', ' ').title()}:[/cyan] {value}\n"
        
        console.print(Panel(
            stats_text.rstrip(),
            title="📊 Statistics",
            style="green"
        ))
    
    def show_config_info(self, config: Config):
        """Display current configuration"""
        config.show_current_config()
    
    def show_help(self):
        """Display help information"""
        help_text = """
[cyan]📝 Task Management Commands:[/cyan]
• [green]add[/green] - Add a new task with date, duration, name and description
• [blue]edit[/blue] - Modify an existing task (select by number)
• [red]delete[/red] - Remove a specific task (select by number)

[cyan]👀 View Commands:[/cyan]
• [green]list[/green] - Show all tasks in a beautiful table
• [magenta]filter[/magenta] - Filter tasks by date, status, priority or search term
• [cyan]today[/cyan] - Quick view of today's tasks only

[cyan]⚙️ System Commands:[/cyan]
• [blue]config[/blue] - Show or modify configuration
• [blue]stats[/blue] - Show task statistics
• [blue]export[/blue] - Export tasks to file
• [blue]import[/blue] - Import tasks from file
• [blue]help[/blue] - Show this detailed help
• [red]clear[/red] - Delete ALL tasks (with confirmation)
• [yellow]exit[/yellow] - Exit the program

[cyan]🎮 Navigation:[/cyan]
• Use ↑↓ arrow keys to navigate menus
• Press Enter to select options
• Press Q to quit at any time
• Use number keys for quick selection

[cyan]📅 Date Format:[/cyan]
Supports both Jalali and Gregorian calendars (configurable)

[cyan]⏱️ Duration Examples:[/cyan]
• 2h (2 hours)
• 30min (30 minutes)
• 1h 30min (1 hour 30 minutes)
• 45m (45 minutes)

[cyan]🏷️ Task Status:[/cyan]
• pending, in_progress, completed, cancelled

[cyan]⚡ Priority Levels:[/cyan]
• low, normal, high, critical
"""
        
        console.print(Panel(
            help_text,
            title="📚 Help & Usage Guide",
            style="blue"
        ))
    
    def show_error(self, message: str):
        """Display error message"""
        console.print(f"[red]❌ {message}[/red]")
    
    def show_success(self, message: str):
        """Display success message"""
        console.print(f"[bold green]✅ {message}[/bold green]")
    
    def show_warning(self, message: str):
        """Display warning message"""
        console.print(f"[yellow]⚠️ {message}[/yellow]")
    
    def show_info(self, message: str):
        """Display info message"""
        console.print(f"[blue]ℹ️ {message}[/blue]")
    
    def show_loading(self, message: str = "Loading..."):
        """Display loading message"""
        console.print(f"[cyan]⏳ {message}[/cyan]")
    
    def show_divider(self, title: str = ""):
        """Show a divider line"""
        console.rule(f"[bold cyan]{title}[/bold cyan]" if title else "")
    
    def show_welcome_message(self):
        """Show welcome message for first-time users"""
        welcome_text = """
[bold cyan]Welcome to Task CLI Manager! 🚀[/bold cyan]

This is your first time using the application. 
Let's get you set up with a quick configuration.

Features you'll love:
• Beautiful terminal interface with arrow key navigation
• Flexible task management with duration tracking
• Jalali date support for Persian users
• Automatic backups and data safety
• Powerful filtering and search capabilities
• Configurable settings for your workflow

Let's start with the initial setup...
"""
        
        console.print(Panel(
            welcome_text,
            title="🎉 Welcome",
            style="bright_green"
        ))
    
    def clear_screen(self):
        """Clear the terminal screen"""
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def pause(self, message: str = "Press any key to continue..."):
        """Pause and wait for user input"""
        console.print(f"[dim]{message}[/dim]")
        try:
            if os.name == 'nt':
                import msvcrt
                msvcrt.getch()
            else:
                input()
        except KeyboardInterrupt:
            pass
