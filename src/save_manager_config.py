"""SaveManagerConfig dataclass for save manager configuration."""
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class SaveManagerConfig:
    """Configuration data for the save manager."""
    username: str
    main_save_path: Path
    backup_directory: Path
    local_backup_directory: Path
    custom_save_folder: Optional[Path] = None  # User-specified custom save folder path
    game_executable_path: Optional[Path] = None  # Path to game executable

