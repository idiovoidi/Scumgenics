"""BackupInfo dataclass for backup file information."""
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass
class BackupInfo:
    """Represents information about a backup save file."""
    filename: str           # e.g., "steamcampaign01_2024-01-15_14-30.savbackup"
    full_path: Path         # Complete file system path
    timestamp: datetime     # Parsed from filename
    size_bytes: int         # File size for display
    
    def display_name(self) -> str:
        """Return formatted display name for UI."""
        # Format: "Jan 15, 2024  2:30 PM  •  123 KB"
        date_str = self.timestamp.strftime('%b %d, %Y')
        time_str = self.timestamp.strftime('%I:%M %p').lstrip('0')
        size_kb = self.size_bytes // 1024
        return f"{date_str}  {time_str}  •  {size_kb} KB"
