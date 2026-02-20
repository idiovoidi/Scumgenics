"""PathBuilder module for constructing file system paths for Mewgenics save files."""

from pathlib import Path
from datetime import datetime
from typing import Optional
import re


class PathBuilder:
    """Constructs file system paths based on username and conventions."""
    
    # Constants for path construction
    GAME_DIRECTORY_TEMPLATE = r"C:\Users\{username}\AppData\Roaming\Glaiel Games\Mewgenics\76561197960287930\saves"
    MAIN_SAVE_FILENAME = "steamcampaign01.sav"
    BACKUP_SUBDIRECTORY = "backups"
    BACKUP_FILENAME_PATTERN = r"steamcampaign01_\d{4}-\d{2}-\d{2}_\d{2}-\d{2}\.savbackup"
    
    @staticmethod
    def build_main_save_path(username: str) -> Path:
        """Build path to main save file.
        
        Args:
            username: Windows username
            
        Returns:
            Path to the main save file
        """
        game_dir = PathBuilder.GAME_DIRECTORY_TEMPLATE.format(username=username)
        return Path(game_dir) / PathBuilder.MAIN_SAVE_FILENAME
    
    @staticmethod
    def build_backup_directory_path(username: str) -> Path:
        """Build path to backup directory.
        
        Args:
            username: Windows username
            
        Returns:
            Path to the backup directory
        """
        game_dir = PathBuilder.GAME_DIRECTORY_TEMPLATE.format(username=username)
        return Path(game_dir) / PathBuilder.BACKUP_SUBDIRECTORY
    
    @staticmethod
    def build_backup_filename(timestamp: datetime) -> str:
        """Build backup filename with timestamp.
        
        Args:
            timestamp: Datetime object for the backup
            
        Returns:
            Backup filename in format steamcampaign01_YYYY-MM-DD_HH-MM.savbackup
        """
        formatted_time = timestamp.strftime("%Y-%m-%d_%H-%M")
        return f"steamcampaign01_{formatted_time}.savbackup"
    
    @staticmethod
    def parse_backup_timestamp(filename: str) -> Optional[datetime]:
        """Extract timestamp from backup filename.
        
        Args:
            filename: Backup filename to parse
            
        Returns:
            Datetime object if parsing succeeds, None otherwise
        """
        # Pattern to extract timestamp from filename
        pattern = r"steamcampaign01_(\d{4})-(\d{2})-(\d{2})_(\d{2})-(\d{2})\.savbackup"
        match = re.match(pattern, filename)
        
        if not match:
            return None
        
        try:
            year, month, day, hour, minute = map(int, match.groups())
            return datetime(year, month, day, hour, minute)
        except (ValueError, TypeError):
            return None
