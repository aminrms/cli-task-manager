"""
Configuration Management Module
Handles application settings and first-time setup
"""

import os
import json
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel

console = Console()

class Config:
    """Application configuration manager"""
    
    def __init__(self):
        self.config_dir = Path.home() / ".task-cli"
        self.config_file = self.config_dir / "config.json"
        self.config = self._load_config()
    
    def _load_config(self) -> dict:
        """Load configuration from file or create default"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                console.print(f"[red]❌ Error loading config: {e}[/red]")
                return self._get_default_config()
        else:
            return self._get_default_config()
    
    def _get_default_config(self) -> dict:
        """Get default configuration"""
        return {
            "csv_file": str(Path("F:/Sepano-Project") / "تایم های کاری.csv"),
            "date_format": "jalali",
            "default_duration": "1h",
            "theme": "default",
            "language": "en",
            "auto_backup": True,
            "backup_count": 5,
            "first_run": True
        }
    
    def save_config(self):
        """Save current configuration to file"""
        try:
            self.config_dir.mkdir(exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except IOError as e:
            console.print(f"[red]❌ Error saving config: {e}[/red]")
    
    def first_time_setup(self):
        """Run first-time setup wizard"""
        if not self.config.get("first_run", True):
            return
        
        console.print(Panel(
            "[bold cyan]Welcome to Task CLI Manager![/bold cyan]\n\n"
            "Let's set up your preferences for the first time.",
            title="🚀 First Time Setup",
            style="bright_blue"
        ))
        
        # CSV file location
        console.print("\n[bold yellow]📁 CSV File Location[/bold yellow]")
        console.print("Where would you like to store your tasks?")
        
        default_path = self.config["csv_file"]
        csv_path = Prompt.ask(
            "Enter CSV file path",
            default=default_path
        )
        
        # Validate and fix path
        csv_path = Path(csv_path)
        
        # If path is a directory, add the default filename
        if csv_path.is_dir() or not csv_path.suffix:
            csv_path = csv_path / "تایم های کاری.csv"
        
        # Create directory if needed
        try:
            csv_path.parent.mkdir(parents=True, exist_ok=True)
            # Test write permissions
            test_file = csv_path.parent / "test_write.tmp"
            test_file.touch()
            test_file.unlink()
            self.config["csv_file"] = str(csv_path)
        except (OSError, PermissionError) as e:
            console.print(f"[red]❌ Cannot access path {csv_path}: {e}[/red]")
            console.print("[yellow]Using default location instead[/yellow]")
            fallback_path = Path.home() / "Documents" / "tasks.csv"
            fallback_path.parent.mkdir(parents=True, exist_ok=True)
            self.config["csv_file"] = str(fallback_path)
        
        # Date format preference
        console.print("\n[bold yellow]📅 Date Format[/bold yellow]")
        date_format = Prompt.ask(
            "Choose date format",
            choices=["jalali", "gregorian"],
            default="jalali"
        )
        self.config["date_format"] = date_format
        
        # Default duration
        console.print("\n[bold yellow]⏱️ Default Task Duration[/bold yellow]")
        default_duration = Prompt.ask(
            "Default duration for new tasks",
            default="1h"
        )
        self.config["default_duration"] = default_duration
        
        # Auto backup
        console.print("\n[bold yellow]💾 Backup Settings[/bold yellow]")
        auto_backup = Confirm.ask(
            "Enable automatic backups?",
            default=True
        )
        self.config["auto_backup"] = auto_backup
        
        # Mark setup as complete
        self.config["first_run"] = False
        self.save_config()
        
        console.print(Panel(
            "[bold green]✅ Setup complete![/bold green]\n\n"
            f"CSV file: {self.config['csv_file']}\n"
            f"Date format: {self.config['date_format']}\n"
            f"Default duration: {self.config['default_duration']}\n"
            f"Auto backup: {self.config['auto_backup']}",
            title="🎉 Configuration Saved",
            style="green"
        ))
    
    def get(self, key: str, default=None):
        """Get configuration value"""
        return self.config.get(key, default)
    
    def set(self, key: str, value):
        """Set configuration value"""
        self.config[key] = value
        self.save_config()
    
    def get_csv_file(self) -> str:
        """Get CSV file path"""
        return self.config["csv_file"]
    
    def get_date_format(self) -> str:
        """Get preferred date format"""
        return self.config.get("date_format", "jalali")
    
    def get_default_duration(self) -> str:
        """Get default task duration"""
        return self.config.get("default_duration", "1h")
    
    def is_first_run(self) -> bool:
        """Check if this is the first run"""
        return self.config.get("first_run", True)
    
    def show_current_config(self):
        """Display current configuration"""
        console.print(Panel(
            f"[cyan]📁 CSV File:[/cyan] {self.config['csv_file']}\n"
            f"[cyan]📅 Date Format:[/cyan] {self.config['date_format']}\n"
            f"[cyan]⏱️ Default Duration:[/cyan] {self.config['default_duration']}\n"
            f"[cyan]💾 Auto Backup:[/cyan] {self.config['auto_backup']}\n"
            f"[cyan]🎨 Theme:[/cyan] {self.config['theme']}",
            title="⚙️ Current Configuration",
            style="blue"
        ))
    
    def reconfigure(self):
        """Run configuration wizard again"""
        self.config["first_run"] = True
        self.first_time_setup()
    
    def fix_csv_path(self):
        """Fix CSV file path if it points to a directory"""
        csv_path = Path(self.config["csv_file"])
        
        if csv_path.is_dir() or not csv_path.suffix:
            fixed_path = csv_path / "تایم های کاری.csv"
            console.print(f"[yellow]⚠️ Fixing CSV path: {csv_path} → {fixed_path}[/yellow]")
            
            try:
                fixed_path.parent.mkdir(parents=True, exist_ok=True)
                self.config["csv_file"] = str(fixed_path)
                self.save_config()
                console.print("[green]✅ CSV path fixed successfully![/green]")
                return True
            except (OSError, PermissionError) as e:
                console.print(f"[red]❌ Cannot fix path: {e}[/red]")
                return False
        
        return True
