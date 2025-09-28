"""
Task Model Module
Defines the Task class and related data structures
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, Dict, Any
import jdatetime

@dataclass
class Task:
    """Task data model"""
    
    date: str
    duration: str
    task: str
    description: str
    id: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    status: str = "completed"
    priority: str = "normal"
    tags: List[str] = None
    
    def __post_init__(self):
        """Initialize default values after creation"""
        if self.tags is None:
            self.tags = []
        
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()
        
        self.updated_at = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert task to dictionary"""
        return {
            'id': self.id,
            'date': self.date,
            'duration': self.duration,
            'task': self.task,
            'description': self.description,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'status': self.status,
            'priority': self.priority,
            'tags': ','.join(self.tags) if self.tags else ''
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Task':
        """Create task from dictionary"""
        tags = data.get('tags', '').split(',') if data.get('tags') else []
        tags = [tag.strip() for tag in tags if tag.strip()]
        
        return cls(
            id=data.get('id'),
            date=data.get('date', ''),
            duration=data.get('duration', '1h'),
            task=data.get('task', ''),
            description=data.get('description', ''),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at'),
            status=data.get('status', 'pending'),
            priority=data.get('priority', 'normal'),
            tags=tags
        )
    
    @classmethod
    def from_csv_row(cls, row: Dict[str, str], task_id: int = None) -> 'Task':
        """Create task from CSV row (backward compatibility)"""
        # Handle both old 'hour' and new 'duration' columns
        duration = row.get('duration') or row.get('hour', '1h')
        
        return cls(
            id=task_id,
            date=row.get('date', ''),
            duration=duration,
            task=row.get('task', ''),
            description=row.get('description', ''),
            status=row.get('status', 'completed'),
            priority=row.get('priority', 'normal')
        )
    
    def to_csv_row(self) -> Dict[str, str]:
        """Convert task to CSV row"""
        return {
            'date': self.date,
            'duration': self.duration,
            'task': self.task,
            'description': self.description,
            'status': self.status,
            'priority': self.priority,
            'tags': ','.join(self.tags) if self.tags else ''
        }
    
    def matches_filter(self, filter_type: str, filter_value: str) -> bool:
        """Check if task matches given filter"""
        filter_value = filter_value.lower()
        
        if filter_type == "date":
            return self.date == filter_value
        elif filter_type == "search":
            return (filter_value in self.task.lower() or 
                   filter_value in self.description.lower() or
                   any(filter_value in tag.lower() for tag in self.tags))
        elif filter_type == "status":
            return self.status.lower() == filter_value
        elif filter_type == "priority":
            return self.priority.lower() == filter_value
        elif filter_type == "tag":
            return any(tag.lower() == filter_value for tag in self.tags)
        
        return False
    
    def is_today(self, date_format: str = "jalali") -> bool:
        """Check if task is scheduled for today"""
        if date_format == "jalali":
            today = jdatetime.date.today().isoformat()
        else:
            today = datetime.now().date().isoformat()
        
        return self.date == today
    
    def get_display_duration(self) -> str:
        """Get formatted duration for display"""
        return self.duration
    
    def get_display_date(self, format_type: str = "jalali") -> str:
        """Get formatted date for display"""
        try:
            if format_type == "jalali":
                jdate = jdatetime.date.fromisoformat(self.date)
                return jdate.strftime("%Y/%m/%d")
            else:
                # Assume it's already in the correct format
                return self.date
        except (ValueError, AttributeError):
            return self.date
    
    def update(self, **kwargs):
        """Update task fields"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        
        self.updated_at = datetime.now().isoformat()
    
    def add_tag(self, tag: str):
        """Add a tag to the task"""
        if tag and tag not in self.tags:
            self.tags.append(tag)
            self.updated_at = datetime.now().isoformat()
    
    def remove_tag(self, tag: str):
        """Remove a tag from the task"""
        if tag in self.tags:
            self.tags.remove(tag)
            self.updated_at = datetime.now().isoformat()
    
    def __str__(self) -> str:
        """String representation of task"""
        return f"{self.date} - {self.task} ({self.duration})"
    
    def __repr__(self) -> str:
        """Detailed string representation"""
        return f"Task(id={self.id}, date='{self.date}', task='{self.task}', duration='{self.duration}')"
