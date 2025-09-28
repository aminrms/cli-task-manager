"""
Application Controller
Main application logic and command handling
"""

from typing import Optional, List
from rich.console import Console

from .core.config import Config
from .core.data_manager import DataManager
from .core.task import Task
from .ui.display import UIManager
from .ui.input_handler import InputHandler
from .utils.navigation import NavigationMenu, MenuOption, create_menu_options

console = Console()

class TaskManager:
    """Main application controller"""
    
    def __init__(self):
        self.config = Config()
        self.data_manager = DataManager(self.config)
        self.ui = UIManager(self.config)
        self.input_handler = InputHandler(self.config)
        self.navigation = NavigationMenu("Task CLI Manager")
        self.running = True
    
    def run(self):
        """Main application loop"""
        # First time setup
        if self.config.is_first_run():
            self.ui.show_welcome_message()
            self.config.first_time_setup()
            # Reinitialize data manager with new config
            self.data_manager = DataManager(self.config)
        else:
            # Check and fix CSV path if needed
            if not self.config.fix_csv_path():
                self.ui.show_error("Configuration error. Please reconfigure.")
                self.config.reconfigure()
            # Reinitialize data manager after potential fix
            self.data_manager = DataManager(self.config)
        
        # Main loop
        while self.running:
            try:
                choice = self._show_main_menu()
                self._handle_choice(choice)
            except KeyboardInterrupt:
                self.ui.show_info("Goodbye!")
                break
            except Exception as e:
                self.ui.show_error(f"Unexpected error: {e}")
    
    def _show_main_menu(self) -> str:
        """Show main navigation menu"""
        menu_options = [
            MenuOption("🆕 Add New Task", "add"),
            MenuOption("📋 List All Tasks", "list"),
            MenuOption("✏️ Edit Task", "edit"),
            MenuOption("🗑️ Delete Task", "delete"),
            MenuOption("🔍 Filter/Search Tasks", "filter"),
            MenuOption("📅 Today's Tasks", "today"),
            MenuOption("📊 Statistics", "stats"),
            MenuOption("⚙️ Configuration", "config"),
            MenuOption("📚 Help & Guide", "help"),
            MenuOption("🗑️ Clear All Tasks", "clear"),
            MenuOption("💾 Import/Export", "import_export"),
            MenuOption("👋 Exit Program", "exit")
        ]
        
        return self.navigation.show_menu(menu_options)
    
    def _handle_choice(self, choice: str):
        """Handle menu choice"""
        handlers = {
            "add": self._add_task,
            "list": self._list_tasks,
            "edit": self._edit_task,
            "delete": self._delete_task,
            "filter": self._filter_tasks,
            "today": self._show_today_tasks,
            "stats": self._show_statistics,
            "config": self._manage_config,
            "help": self._show_help,
            "clear": self._clear_all_tasks,
            "import_export": self._import_export_menu,
            "exit": self._exit_app
        }
        
        handler = handlers.get(choice)
        if handler:
            handler()
        else:
            self.ui.show_error(f"Unknown choice: {choice}")
    
    def _add_task(self):
        """Add new task"""
        self.ui.show_divider("Add New Task")
        
        task = self.input_handler.get_task_input()
        if task:
            if self.data_manager.add_task(task):
                self.ui.show_success(f"Task '{task.task}' added successfully!")
            else:
                self.ui.show_error("Failed to add task")
        
        self.ui.pause()
    
    def _list_tasks(self):
        """List all tasks"""
        self.ui.show_divider("All Tasks")
        
        tasks = self.data_manager.load_tasks()
        self.ui.show_tasks_table(tasks)
        
        self.ui.pause()
    
    def _edit_task(self):
        """Edit existing task"""
        self.ui.show_divider("Edit Task")
        
        tasks = self.data_manager.load_tasks()
        if not tasks:
            self.ui.show_warning("No tasks to edit")
            self.ui.pause()
            return
        
        # Show tasks and get selection
        self.ui.show_tasks_table(tasks, "Select Task to Edit")
        
        task_index = self.input_handler.get_number_input(
            f"Enter task number (1-{len(tasks)}, 0 to cancel)",
            min_val=0,
            max_val=len(tasks)
        )
        
        if task_index is None or task_index == 0:
            return
        
        # Get task to edit
        current_task = tasks[task_index - 1]
        
        # Show current task details
        self.ui.show_task_details(current_task, "Current Task")
        
        # Get updated task
        updated_task = self.input_handler.get_task_input(current_task)
        if updated_task:
            if self.data_manager.update_task(task_index - 1, updated_task):
                self.ui.show_success("Task updated successfully!")
            else:
                self.ui.show_error("Failed to update task")
        
        self.ui.pause()
    
    def _delete_task(self):
        """Delete task"""
        self.ui.show_divider("Delete Task")
        
        tasks = self.data_manager.load_tasks()
        if not tasks:
            self.ui.show_warning("No tasks to delete")
            self.ui.pause()
            return
        
        # Show tasks and get selection
        self.ui.show_tasks_table(tasks, "Select Task to Delete")
        
        task_index = self.input_handler.get_number_input(
            f"Enter task number (1-{len(tasks)}, 0 to cancel)",
            min_val=0,
            max_val=len(tasks)
        )
        
        if task_index is None or task_index == 0:
            return
        
        # Show task to delete
        task_to_delete = tasks[task_index - 1]
        self.ui.show_task_details(task_to_delete, "Task to Delete")
        
        # Confirm deletion
        if self.input_handler.confirm_action("⚠️ Delete this task?", default=False):
            if self.data_manager.delete_task(task_index - 1):
                self.ui.show_success("Task deleted successfully!")
            else:
                self.ui.show_error("Failed to delete task")
        
        self.ui.pause()
    
    def _filter_tasks(self):
        """Filter and search tasks"""
        self.ui.show_divider("Filter Tasks")
        
        filter_menu = NavigationMenu("Filter Options")
        filter_options = [
            MenuOption("📅 Filter by Date", "date"),
            MenuOption("🔍 Search Tasks", "search"),
            MenuOption("🏷️ Filter by Status", "status"),
            MenuOption("⚡ Filter by Priority", "priority"),
            MenuOption("🔙 Back to Main Menu", "back")
        ]
        
        choice = filter_menu.show_menu(filter_options)
        
        if choice == "back":
            return
        
        filtered_tasks = []
        
        if choice == "date":
            date = self.input_handler.get_filter_date()
            if date:
                filtered_tasks = self.data_manager.filter_tasks("date", date)
                
        elif choice == "search":
            query = self.input_handler.get_search_query()
            if query:
                filtered_tasks = self.data_manager.search_tasks(query)
                
        elif choice == "status":
            status = self.input_handler.get_selection(
                "Select status",
                ["pending", "in_progress", "completed", "cancelled"]
            )
            if status:
                filtered_tasks = self.data_manager.get_tasks_by_status(status)
                
        elif choice == "priority":
            priority = self.input_handler.get_selection(
                "Select priority",
                ["low", "normal", "high", "critical"]
            )
            if priority:
                filtered_tasks = self.data_manager.get_tasks_by_priority(priority)
        
        if filtered_tasks is not None:
            self.ui.show_tasks_table(filtered_tasks, f"Filtered Tasks ({choice})")
        
        self.ui.pause()
    
    def _show_today_tasks(self):
        """Show today's tasks"""
        self.ui.show_divider("Today's Tasks")
        
        today_tasks = self.data_manager.get_today_tasks()
        self.ui.show_tasks_table(today_tasks, "📅 Today's Tasks")
        
        self.ui.pause()
    
    def _show_statistics(self):
        """Show task statistics"""
        self.ui.show_divider("Statistics")
        
        tasks = self.data_manager.load_tasks()
        
        stats = {
            "total_tasks": len(tasks),
            "completed_tasks": len([t for t in tasks if t.status == "completed"]),
            "pending_tasks": len([t for t in tasks if t.status == "pending"]),
            "in_progress_tasks": len([t for t in tasks if t.status == "in_progress"]),
            "cancelled_tasks": len([t for t in tasks if t.status == "cancelled"]),
            "high_priority_tasks": len([t for t in tasks if t.priority == "high"]),
            "critical_priority_tasks": len([t for t in tasks if t.priority == "critical"]),
            "today_tasks": len(self.data_manager.get_today_tasks())
        }
        
        # Add data file info
        data_info = self.data_manager.get_data_info()
        stats.update({
            "csv_file_size": f"{data_info['file_size']} bytes",
            "backup_count": data_info['backup_count'],
            "last_modified": data_info['last_modified']
        })
        
        self.ui.show_statistics(stats)
        self.ui.pause()
    
    def _manage_config(self):
        """Manage configuration"""
        self.ui.show_divider("Configuration")
        
        config_menu = NavigationMenu("Configuration Options")
        config_options = [
            MenuOption("👀 Show Current Config", "show"),
            MenuOption("✏️ Update Configuration", "update"),
            MenuOption("🔄 Reset to Defaults", "reset"),
            MenuOption("🔙 Back to Main Menu", "back")
        ]
        
        choice = config_menu.show_menu(config_options)
        
        if choice == "show":
            self.ui.show_config_info(self.config)
        elif choice == "update":
            updated_config = self.input_handler.get_config_update(self.config.config)
            for key, value in updated_config.items():
                self.config.set(key, value)
            self.ui.show_success("Configuration updated!")
            # Reinitialize data manager
            self.data_manager = DataManager(self.config)
        elif choice == "reset":
            if self.input_handler.confirm_action("Reset all settings to defaults?"):
                self.config.config = self.config._get_default_config()
                self.config.save_config()
                self.ui.show_success("Configuration reset to defaults!")
        
        if choice != "back":
            self.ui.pause()
    
    def _show_help(self):
        """Show help information"""
        self.ui.show_divider("Help & Guide")
        self.ui.show_help()
        self.ui.pause()
    
    def _clear_all_tasks(self):
        """Clear all tasks"""
        self.ui.show_divider("Clear All Tasks")
        
        task_count = self.data_manager.get_task_count()
        if task_count == 0:
            self.ui.show_warning("No tasks to clear")
            self.ui.pause()
            return
        
        if self.input_handler.confirm_action(
            f"⚠️ Delete ALL {task_count} tasks? This cannot be undone!",
            default=False
        ):
            if self.data_manager.clear_all_tasks():
                self.ui.show_success("All tasks cleared successfully!")
            else:
                self.ui.show_error("Failed to clear tasks")
        
        self.ui.pause()
    
    def _import_export_menu(self):
        """Import/Export menu"""
        self.ui.show_divider("Import/Export")
        
        ie_menu = NavigationMenu("Import/Export Options")
        ie_options = [
            MenuOption("📤 Export Tasks", "export"),
            MenuOption("📥 Import Tasks", "import"),
            MenuOption("💾 Backup Data", "backup"),
            MenuOption("🔙 Back to Main Menu", "back")
        ]
        
        choice = ie_menu.show_menu(ie_options)
        
        if choice == "export":
            path = self.input_handler.get_export_path()
            if path:
                if self.data_manager.export_data(path):
                    self.ui.show_success(f"Data exported to {path}")
                else:
                    self.ui.show_error("Export failed")
                    
        elif choice == "import":
            path = self.input_handler.get_import_path()
            if path:
                if self.data_manager.import_data(path):
                    self.ui.show_success(f"Data imported from {path}")
                else:
                    self.ui.show_error("Import failed")
                    
        elif choice == "backup":
            self.data_manager.backup_data()
            self.ui.show_success("Manual backup created")
        
        if choice != "back":
            self.ui.pause()
    
    def _exit_app(self):
        """Exit application"""
        self.ui.show_info("Thanks for using Task CLI Manager!")
        self.running = False
