#!/usr/bin/env python3
"""
Beautiful Task CLI Manager
A terminal-based task manager with beautiful UI using Rich library
Supports Jalali date system and stores tasks in custom CSV location
"""

import csv
import os
import sys
import re
import jdatetime
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm, IntPrompt
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich.columns import Columns
from rich.tree import Tree
import msvcrt

console = Console()

# Store CSV file in F:\Sepano-Project with Persian name
CSV_FILE = r"F:\Sepano-Project\تایم های کاری.csv"

def parse_duration_to_minutes(duration_str):
    """Parse duration string to minutes (e.g., '2h', '30min', '1h 30min')"""
    if not duration_str:
        return 60  # Default 1 hour
    
    total_minutes = 0
    duration_str = duration_str.lower().strip()
    
    # Handle formats like '2h', '30min', '1h 30min', '45m'
    # Find hours
    hours_match = re.search(r'(\d+)h', duration_str)
    if hours_match:
        total_minutes += int(hours_match.group(1)) * 60
    
    # Find minutes
    minutes_match = re.search(r'(\d+)(?:min|m)(?!h)', duration_str)
    if minutes_match:
        total_minutes += int(minutes_match.group(1))
    
    # If no format found, assume it's hours
    if total_minutes == 0:
        try:
            total_minutes = float(duration_str) * 60
        except ValueError:
            total_minutes = 60  # Default 1 hour
    
    return total_minutes

def calculate_total_duration(tasks):
    """Calculate total duration of all tasks in hours"""
    total_minutes = 0
    
    for task in tasks:
        duration_key = "duration" if "duration" in task else "hour"
        duration_str = task.get(duration_key, "1h")
        total_minutes += parse_duration_to_minutes(duration_str)
    
    # Convert to hours with 2 decimal places
    total_hours = total_minutes / 60
    return round(total_hours, 2)

def get_key():
    """Get a single keypress from user"""
    if os.name == 'nt':  # Windows
        while True:
            key = msvcrt.getch()
            if key == b'\xe0':  # Arrow key prefix on Windows
                key = msvcrt.getch()
                if key == b'H':  # Up arrow
                    return 'up'
                elif key == b'P':  # Down arrow
                    return 'down'
            elif key == b'\r':  # Enter key
                return 'enter'
            elif key == b'\x1b':  # Escape key
                return 'escape'
            elif key in [b'q', b'Q']:
                return 'quit'
    else:  # Unix/Linux/Mac
        import termios, tty
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            key = sys.stdin.read(1)
            if key == '\x1b':  # Escape sequence
                key += sys.stdin.read(2)
                if key == '\x1b[A':
                    return 'up'
                elif key == '\x1b[B':
                    return 'down'
                else:
                    return 'escape'
            elif key == '\r' or key == '\n':
                return 'enter'
            elif key.lower() == 'q':
                return 'quit'
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
    return None

def arrow_menu(options, title="Choose an option"):
    """Create an interactive arrow key menu"""
    selected = 0
    
    # Show header once
    show_header()
    
    def display_menu():
        """Display the menu"""
        console.print(Panel(
            f"[bold cyan]Use ↑↓ arrows to navigate, Enter to select, Q to quit[/bold cyan]",
            title=f"🎯 {title}",
            style="bright_blue"
        ))
        
        # Show options with highlighting
        for i, option in enumerate(options):
            if i == selected:
                console.print(f"[black on bright_green]❯ {option['display']}[/black on bright_green]")
            else:
                console.print(f"  {option['display']}")
        
        console.print()
        console.print("[dim]Use ↑↓ to navigate, Enter to select[/dim]")
    
    def update_menu():
        """Update menu by clearing screen and redrawing"""
        # Clear screen and redraw header
        os.system('cls' if os.name == 'nt' else 'clear')
        show_header()
        
        # Redraw menu
        console.print(Panel(
            f"[bold cyan]Use ↑↓ arrows to navigate, Enter to select, Q to quit[/bold cyan]",
            title=f"🎯 {title}",
            style="bright_blue"
        ))
        
        # Redraw options
        for i, option in enumerate(options):
            if i == selected:
                console.print(f"[black on bright_green]❯ {option['display']}[/black on bright_green]")
            else:
                console.print(f"  {option['display']}")
        
        console.print()
        console.print("[dim]Use ↑↓ to navigate, Enter to select[/dim]")
    
    # Initial display
    display_menu()
    
    while True:
        # Get user input
        key = get_key()
        
        if key == 'up':
            selected = (selected - 1) % len(options)
            update_menu()
        elif key == 'down':
            selected = (selected + 1) % len(options)
            update_menu()
        elif key == 'enter':
            return options[selected]['value']
        elif key in ['quit', 'escape']:
            return 'exit'

def ensure_csv_directory():
    """Ensure the directory for CSV file exists"""
    csv_dir = os.path.dirname(CSV_FILE)
    if not os.path.exists(csv_dir):
        try:
            os.makedirs(csv_dir, exist_ok=True)
            console.print(f"[green]📁 Created directory: {csv_dir}[/green]")
        except Exception as e:
            console.print(f"[red]❌ Error creating directory {csv_dir}: {e}[/red]")
            sys.exit(1)

def ensure_csv_file():
    """Ensure CSV file exists with proper headers"""
    ensure_csv_directory()
    
    if not os.path.exists(CSV_FILE):
        try:
            with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["date", "duration", "task", "description"])
            console.print(f"[green]📋 Created tasks file: {CSV_FILE}[/green]")
        except Exception as e:
            console.print(f"[red]❌ Error creating CSV file: {e}[/red]")
            sys.exit(1)

def show_header():
    """Display beautiful header"""
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

def add_task():
    """Add a new task with beautiful prompts"""
    console.rule("[bold green]📝 Add New Task[/bold green]")
    console.print()

    # Get current Jalali date as default
    current_jalali = jdatetime.date.today().isoformat()
    
    try:
        date = Prompt.ask(
            "📅 Enter date (Jalali format YYYY-MM-DD)", 
            default=current_jalali
        )
        
        # Validate Jalali date
        jdate = jdatetime.date.fromisoformat(date)
        date_str = jdate.isoformat()
        
        duration = Prompt.ask("⏱️ Enter duration (e.g., 2h, 30min, 1h 30min)", default="1h")
        task = Prompt.ask("📝 Enter task name")
        description = Prompt.ask("📖 Enter task description", default="")

        # Confirm before saving
        console.print()
        console.print(Panel(
            f"[cyan]📅 Date:[/cyan] {date_str}\n"
            f"[yellow]⏱️ Duration:[/yellow] {duration}\n"
            f"[green]📝 Task:[/green] {task}\n"
            f"[white]📖 Description:[/white] {description}",
            title="Task Preview",
            style="blue"
        ))
        
        if Confirm.ask("💾 Save this task?", default=True):
            with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow([date_str, duration, task, description])
            
            console.print(f"[bold green]✅ Task '{task}' added successfully![/bold green]")
        else:
            console.print("[yellow]❌ Task not saved.[/yellow]")
            
    except ValueError as e:
        console.print(f"[red]❌ Invalid Jalali date format! Please use YYYY-MM-DD format.[/red]")
    except Exception as e:
        console.print(f"[red]❌ Error adding task: {e}[/red]")

def get_all_tasks():
    """Get all tasks from CSV file"""
    tasks = []
    if os.path.exists(CSV_FILE):
        try:
            with open(CSV_FILE, mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for idx, row in enumerate(reader, 1):
                    row['id'] = idx
                    tasks.append(row)
        except Exception as e:
            console.print(f"[red]❌ Error reading tasks: {e}[/red]")
    return tasks

def list_tasks(filter_date=None, search_term=None):
    """Display all tasks in a beautiful table with optional filtering"""
    tasks = get_all_tasks()
    
    if not tasks:
        console.print(Panel(
            "[yellow]No tasks found! Use 'add' to create your first task.[/yellow]",
            title="📋 Task List",
            style="yellow"
        ))
        return

    # Apply filters
    filtered_tasks = tasks
    if filter_date:
        filtered_tasks = [task for task in filtered_tasks if task["date"] == filter_date]
    if search_term:
        search_term = search_term.lower()
        filtered_tasks = [task for task in filtered_tasks if 
                         search_term in task["task"].lower() or 
                         search_term in task["description"].lower()]

    if not filtered_tasks:
        console.print(Panel(
            "[yellow]No tasks found matching your criteria![/yellow]",
            title="📋 Filtered Results",
            style="yellow"
        ))
        return

    try:
        table = Table(
            title=f"📋 Your Task Schedule ({len(filtered_tasks)} tasks)", 
            show_lines=True,
            title_style="bold cyan"
        )
        
        table.add_column("#", style="dim", width=3)
        table.add_column("📅 Date", style="cyan", no_wrap=True, width=12)
        table.add_column("⏱️ Duration", style="yellow", width=10)
        table.add_column("📝 Task", style="green", min_width=15)
        table.add_column("📖 Description", style="white", min_width=20)

        for task in filtered_tasks:
            duration_key = "duration" if "duration" in task else "hour"
            table.add_row(
                str(task['id']),
                task["date"], 
                task.get(duration_key, "1h"), 
                task["task"], 
                task["description"]
            )

        console.print(table)
        
        # Calculate and show total duration
        total_hours = calculate_total_duration(filtered_tasks)
        console.print(f"[bold green]⏱️ Total Duration: {total_hours} hours[/bold green]")
        
        # Show filter info if applied
        filter_info = []
        if filter_date:
            filter_info.append(f"Date: {filter_date}")
        if search_term:
            filter_info.append(f"Search: '{search_term}'")
        if filter_info:
            console.print(f"[dim]Filters applied: {', '.join(filter_info)}[/dim]")
        
        console.print(f"[dim]Total matching tasks: {len(filtered_tasks)} / {len(tasks)}[/dim]")
            
    except Exception as e:
        console.print(f"[red]❌ Error displaying tasks: {e}[/red]")

def delete_task_interactive():
    """Delete a specific task using interactive selection"""
    tasks = get_all_tasks()
    if not tasks:
        console.print("[yellow]No tasks to delete.[/yellow]")
        return
    
    console.rule("[bold red]🗑️  Delete Specific Task[/bold red]")
    
    task_index = select_task_interactive(tasks, "delete")
    
    if task_index is None:
        console.print("[yellow]❌ Delete operation cancelled.[/yellow]")
        return
    
    try:
        task_to_delete = tasks[task_index]
        
        duration_key = "duration" if "duration" in task_to_delete else "hour"
        console.print(Panel(
            f"[cyan]📅 Date:[/cyan] {task_to_delete['date']}\n"
            f"[yellow]⏱️ Duration:[/yellow] {task_to_delete.get(duration_key, '1h')}\n"
            f"[green]📝 Task:[/green] {task_to_delete['task']}\n"
            f"[white]📖 Description:[/white] {task_to_delete['description']}",
            title="Task to Delete",
            style="red"
        ))
        
        if Confirm.ask(f"[red]⚠️  Delete this task?[/red]"):
            # Remove the task and rewrite CSV
            tasks.pop(task_index)
            save_all_tasks(tasks)
            console.print(f"[bold green]✅ Task deleted successfully![/bold green]")
        else:
            console.print("[yellow]❌ Delete operation cancelled.[/yellow]")
            
    except Exception as e:
        console.print(f"[red]❌ Error deleting task: {e}[/red]")

def edit_task_interactive():
    """Edit an existing task using interactive selection"""
    tasks = get_all_tasks()
    if not tasks:
        console.print("[yellow]No tasks to edit.[/yellow]")
        return
    
    console.rule("[bold blue]✏️  Edit Task[/bold blue]")
    
    task_index = select_task_interactive(tasks, "edit")
    
    if task_index is None:
        console.print("[yellow]❌ Edit operation cancelled.[/yellow]")
        return
    
    try:
        task = tasks[task_index]
        
        duration_key = "duration" if "duration" in task else "hour"
        current_duration = task.get(duration_key, "1h")
        
        console.print(Panel(
            f"[cyan]📅 Current Date:[/cyan] {task['date']}\n"
            f"[yellow]⏱️ Current Duration:[/yellow] {current_duration}\n"
            f"[green]📝 Current Task:[/green] {task['task']}\n"
            f"[white]📖 Current Description:[/white] {task['description']}",
            title="Current Task Details",
            style="blue"
        ))
        
        # Get new values (default to current values)
        new_date = Prompt.ask("📅 New date (Jalali YYYY-MM-DD)", default=task['date'])
        new_duration = Prompt.ask("⏱️ New duration (e.g., 2h, 30min, 1h 30min)", default=current_duration)
        new_task = Prompt.ask("📝 New task name", default=task['task'])
        new_description = Prompt.ask("📖 New description", default=task['description'])
        
        # Validate date
        try:
            jdate = jdatetime.date.fromisoformat(new_date)
            new_date = jdate.isoformat()
        except ValueError:
            console.print("[red]❌ Invalid date format![/red]")
            return
        
        # Update task
        tasks[task_index] = {
            'date': new_date,
            'duration': new_duration,
            'task': new_task,
            'description': new_description
        }
        
        save_all_tasks(tasks)
        console.print("[bold green]✅ Task updated successfully![/bold green]")
        
    except Exception as e:
        console.print(f"[red]❌ Error editing task: {e}[/red]")

def save_all_tasks(tasks):
    """Save all tasks back to CSV file"""
    try:
        with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["date", "duration", "task", "description"])
            for task in tasks:
                duration_key = "duration" if "duration" in task else "hour"
                writer.writerow([task["date"], task.get(duration_key, "1h"), task["task"], task["description"]])
    except Exception as e:
        console.print(f"[red]❌ Error saving tasks: {e}[/red]")

def clear_tasks():
    """Clear all tasks with confirmation"""
    if not os.path.exists(CSV_FILE):
        console.print("[yellow]No tasks to clear.[/yellow]")
        return
    
    console.rule("[bold red]🗑️  Clear All Tasks[/bold red]")
    
    if Confirm.ask("[red]⚠️  Are you sure you want to delete ALL tasks? This cannot be undone![/red]"):
        try:
            with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["date", "duration", "task", "description"])
            console.print("[bold green]✅ All tasks cleared successfully![/bold green]")
        except Exception as e:
            console.print(f"[red]❌ Error clearing tasks: {e}[/red]")
    else:
        console.print("[yellow]❌ Clear operation cancelled.[/yellow]")

def filter_tasks_interactive():
    """Filter tasks using interactive menu"""
    console.rule("[bold magenta]🔍 Filter Tasks[/bold magenta]")
    
    filter_type = show_filter_menu()
    
    if filter_type == "date":
        date_filter = Prompt.ask("Enter date to filter (Jalali YYYY-MM-DD)")
        try:
            jdate = jdatetime.date.fromisoformat(date_filter)
            list_tasks(filter_date=jdate.isoformat())
        except ValueError:
            console.print("[red]❌ Invalid date format![/red]")
    elif filter_type == "search":
        search_term = Prompt.ask("Enter search term (task name or description)")
        list_tasks(search_term=search_term)
    elif filter_type == "today":
        today = jdatetime.date.today().isoformat()
        list_tasks(filter_date=today)
    # If "back", just return to main menu

def show_interactive_menu():
    """Display interactive arrow key menu"""
    
    menu_options = [
        {"display": "🆕 Add New Task", "value": "add"},
        {"display": "📋 List All Tasks", "value": "list"},
        {"display": "✏️ Edit Task", "value": "edit"},
        {"display": "🗑️ Delete Task", "value": "delete"},
        {"display": "🔍 Filter/Search Tasks", "value": "filter"},
        {"display": "📅 Today's Tasks", "value": "today"},
        {"display": "📚 Help & Guide", "value": "help"},
        {"display": "🗑️ Clear All Tasks", "value": "clear"},
        {"display": "👋 Exit Program", "value": "exit"}
    ]
    
    return arrow_menu(menu_options, "Task CLI Manager")

def show_filter_menu():
    """Interactive filter menu with arrow keys"""
    filter_options = [
        {"display": "📅 Filter by Date", "value": "date"},
        {"display": "🔍 Search in Tasks", "value": "search"},
        {"display": "📅 Today's Tasks Only", "value": "today"},
        {"display": "🔙 Back to Main Menu", "value": "back"}
    ]
    
    return arrow_menu(filter_options, "Filter Options")

def select_task_interactive(tasks, action="select"):
    """Interactive task selection with arrow keys"""
    if not tasks:
        console.print("[yellow]No tasks available.[/yellow]")
        return None
    
    task_options = []
    for i, task in enumerate(tasks):
        duration_key = "duration" if "duration" in task else "hour"
        duration_value = task.get(duration_key, "1h")
        display = f"{i+1:2d}. 📅 {task['date']} ⏱️ {duration_value} - {task['task']}"
        task_options.append({"display": display, "value": i})
    
    task_options.append({"display": "🔙 Cancel", "value": None})
    
    return arrow_menu(task_options, f"Select Task to {action.title()}")

def show_help():
    """Show detailed help information"""
    help_text = """
[cyan]📝 Task Management Commands:[/cyan]
• [green]add[/green] - Add a new task with date, time, name and description
• [blue]edit[/blue] - Modify an existing task (select by number)
• [red]delete[/red] - Remove a specific task (select by number)

[cyan]👀 View Commands:[/cyan]
• [green]list[/green] - Show all tasks in a beautiful table
• [magenta]filter[/magenta] - Filter tasks by date or search in task/description
• [cyan]today[/cyan] - Quick view of today's tasks only

[cyan]⚙️ System Commands:[/cyan]
• [blue]help[/blue] - Show this detailed help
• [red]clear[/red] - Delete ALL tasks (with confirmation)
• [yellow]exit[/yellow] - Exit the program

[cyan]📅 Date Format:[/cyan]
Use Jalali calendar format: YYYY-MM-DD (e.g., 1403-07-15)

[cyan]⏰ Time Format:[/cyan] 
Use 24-hour format: HH:MM (e.g., 14:30)

[cyan]💾 Data Storage:[/cyan]
Tasks are stored in: F:\\Sepano-Project\\تایم های کاری.csv

[cyan]🔍 Filter Options:[/cyan]
• Filter by specific date
• Search in task names and descriptions
• View today's tasks only
"""
    
    console.print(Panel(
        help_text,
        title="📚 Detailed Help & Usage Guide",
        style="blue"
    ))

def show_today_tasks():
    """Show only today's tasks"""
    today = jdatetime.date.today().isoformat()
    console.rule(f"[bold cyan]📅 Today's Tasks ({today})[/bold cyan]")
    list_tasks(filter_date=today)

def main():
    """Main application loop with interactive arrow key navigation"""
    ensure_csv_file()
    show_header()
    
    while True:
        try:
            console.print()
            choice = show_interactive_menu()
            console.print()
            
            if choice == "add":
                add_task()
            elif choice == "edit":
                edit_task_interactive()
            elif choice == "delete":
                delete_task_interactive()
            elif choice == "list":
                list_tasks()
            elif choice == "filter":
                filter_tasks_interactive()
            elif choice == "today":
                show_today_tasks()
            elif choice == "help":
                show_help()
            elif choice == "clear":
                clear_tasks()
            elif choice == "exit":
                console.print("[bold yellow]👋 Thanks for using Task CLI Manager! Goodbye![/bold yellow]")
                break
                
        except KeyboardInterrupt:
            console.print("\n[yellow]👋 Goodbye![/yellow]")
            break
        except Exception as e:
            console.print(f"[red]❌ Unexpected error: {e}[/red]")

if __name__ == "__main__":
    main()
