"""
Navigation Utilities
Handles keyboard input and menu navigation
"""

import os
import sys
import msvcrt
from typing import List, Dict, Any, Optional

from rich.console import Console

console = Console()

class MenuOption:
    """Represents a menu option"""
    
    def __init__(self, display: str, value: str, description: str = ""):
        self.display = display
        self.value = value
        self.description = description
    
    def __str__(self):
        return self.display

class KeyboardHandler:
    """Handles keyboard input for navigation"""
    
    @staticmethod
    def get_key() -> Optional[str]:
        """Get a single keypress from user"""
        if os.name == 'nt':  # Windows
            try:
                key = msvcrt.getch()
                if key == b'\xe0':  # Arrow key prefix on Windows
                    key = msvcrt.getch()
                    if key == b'H':  # Up arrow
                        return 'up'
                    elif key == b'P':  # Down arrow
                        return 'down'
                    elif key == b'K':  # Left arrow
                        return 'left'
                    elif key == b'M':  # Right arrow
                        return 'right'
                elif key == b'\r':  # Enter key
                    return 'enter'
                elif key == b'\x1b':  # Escape key
                    return 'escape'
                elif key in [b'q', b'Q']:
                    return 'quit'
                elif key == b'\x08':  # Backspace
                    return 'backspace'
                elif key == b' ':  # Space
                    return 'space'
                elif key.isalnum():
                    return key.decode('utf-8').lower()
            except:
                return None
        else:  # Unix/Linux/Mac
            try:
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
                        elif key == '\x1b[C':
                            return 'right'
                        elif key == '\x1b[D':
                            return 'left'
                        else:
                            return 'escape'
                    elif key == '\r' or key == '\n':
                        return 'enter'
                    elif key.lower() == 'q':
                        return 'quit'
                    elif key == '\x7f':  # Backspace/Delete
                        return 'backspace'
                    elif key == ' ':
                        return 'space'
                    elif key.isalnum():
                        return key.lower()
                finally:
                    termios.tcsetattr(fd, termios.TCSADRAIN, old)
            except:
                return None
        return None

class NavigationMenu:
    """Interactive navigation menu with arrow keys"""
    
    def __init__(self, title: str = "Menu", show_instructions: bool = True):
        self.title = title
        self.show_instructions = show_instructions
        self.keyboard = KeyboardHandler()
    
    def show_menu(self, options: List[MenuOption], selected: int = 0) -> str:
        """Display menu and handle navigation"""
        from rich.panel import Panel
        
        # Show header once
        self._show_header()
        
        # Initial display
        self._display_menu(options, selected)
        
        while True:
            # Get user input
            key = self.keyboard.get_key()
            
            if key == 'up':
                selected = (selected - 1) % len(options)
                self._update_menu_display(options, selected)
            elif key == 'down':
                selected = (selected + 1) % len(options)
                self._update_menu_display(options, selected)
            elif key == 'enter':
                return options[selected].value
            elif key in ['quit', 'escape']:
                return 'exit'
            elif key and key.isdigit():
                # Allow numeric selection
                num = int(key) - 1
                if 0 <= num < len(options):
                    return options[num].value
    
    def _display_menu(self, options: List[MenuOption], selected: int):
        """Display the complete menu"""
        from rich.panel import Panel
        
        # Show title panel
        console.print(Panel(f"[bold cyan]{self.title}[/bold cyan]", style="bright_blue"))
        
        # Show menu options
        for i, option in enumerate(options):
            if i == selected:
                console.print(f"[black on bright_green]❯ {option.display}[/black on bright_green]")
            else:
                console.print(f"  {option.display}")
        
        console.print()
        
        # Show instructions
        if self.show_instructions:
            self._show_instructions()
    
    def _update_menu_display(self, options: List[MenuOption], selected: int):
        """Update menu by clearing screen and redrawing"""
        # Clear screen and show header
        self._clear_screen()
        self._show_header()
        
        # Redraw menu
        self._display_menu(options, selected)
    
    def _display_initial_menu(self, options: List[MenuOption], selected: int):
        """Display the initial menu with header"""
        from rich.panel import Panel
        
        # Show header
        self._show_header()
        
        # Show menu title
        console.print(Panel(
            f"[bold cyan]{self.title}[/bold cyan]",
            style="bright_blue"
        ))
        
        # Show options
        for i, option in enumerate(options):
            if i == selected:
                console.print(f"[black on bright_green]❯ {option.display}[/black on bright_green]")
            else:
                console.print(f"  {option.display}")
        
        console.print()
        
        # Show instructions
        if self.show_instructions:
            self._show_instructions()
    
    def _update_menu(self, options: List[MenuOption], selected: int):
        """Update menu options without clearing screen"""
        # Move cursor up to overwrite the menu options
        lines_to_clear = len(options) + 3  # options + title panel + empty line + instructions
        
        # Move cursor up and clear lines
        for _ in range(lines_to_clear):
            console.print("\033[A\033[K", end="")  # Move up and clear line
        
        # Redraw options
        for i, option in enumerate(options):
            if i == selected:
                console.print(f"[black on bright_green]❯ {option.display}[/black on bright_green]")
            else:
                console.print(f"  {option.display}")
        
        console.print()
        
        # Show instructions
        if self.show_instructions:
            self._show_instructions()
    
    def _clear_screen(self):
        """Clear the screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def _show_header(self):
        """Show application header"""
        from ..ui.display import UIManager
        ui = UIManager()
        ui.show_header()
    
    def _display_options(self, options: List[MenuOption], selected: int):
        """Display menu options with highlighting"""
        from rich.panel import Panel
        
        console.print(Panel(
            f"[bold cyan]{self.title}[/bold cyan]",
            style="bright_blue"
        ))
        
        for i, option in enumerate(options):
            if i == selected:
                console.print(f"[black on bright_green]❯ {option.display}[/black on bright_green]")
            else:
                console.print(f"  {option.display}")
        
        console.print()
    
    def _show_instructions(self):
        """Show navigation instructions"""
        console.print("[dim]↑↓ Navigate  Enter Select  Q Quit  1-9 Quick Select[/dim]")

class QuickMenu:
    """Simple menu for quick selections"""
    
    @staticmethod
    def show_options(options: List[str], title: str = "Choose option") -> Optional[str]:
        """Show a simple option menu"""
        from rich.panel import Panel
        from rich.prompt import Prompt
        
        # Display options
        option_text = "\n".join([f"[cyan]{i+1}.[/cyan] {opt}" for i, opt in enumerate(options)])
        console.print(Panel(option_text, title=title, style="blue"))
        
        try:
            choice = Prompt.ask(
                "Enter choice",
                choices=[str(i+1) for i in range(len(options))] + ["0"],
                default="0"
            )
            
            if choice == "0":
                return None
            else:
                return options[int(choice) - 1]
        except (ValueError, IndexError, KeyboardInterrupt):
            return None
    
    @staticmethod
    def confirm(message: str, default: bool = True) -> bool:
        """Show confirmation dialog"""
        from rich.prompt import Confirm
        try:
            return Confirm.ask(message, default=default)
        except KeyboardInterrupt:
            return False

class ProgressMenu:
    """Menu with progress indication"""
    
    def __init__(self, steps: List[str]):
        self.steps = steps
        self.current_step = 0
    
    def next_step(self):
        """Move to next step"""
        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
    
    def previous_step(self):
        """Move to previous step"""
        if self.current_step > 0:
            self.current_step -= 1
    
    def show_progress(self):
        """Show current progress"""
        from rich.progress import Progress, BarColumn, TextColumn
        
        progress = Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        )
        
        task = progress.add_task(
            f"Step {self.current_step + 1}/{len(self.steps)}: {self.steps[self.current_step]}",
            total=len(self.steps)
        )
        
        progress.update(task, completed=self.current_step + 1)
        console.print(progress)

def create_menu_options(items: List[Dict[str, str]]) -> List[MenuOption]:
    """Create MenuOption objects from dictionary list"""
    return [
        MenuOption(
            display=item.get("display", item.get("name", "")),
            value=item.get("value", item.get("key", "")),
            description=item.get("description", "")
        )
        for item in items
    ]
