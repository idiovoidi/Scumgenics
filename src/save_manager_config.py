"""SaveManagerConfig dataclass for save manager configuration."""
from dataclasses import dataclass
from pathlib import Path


@dataclass
class SaveManagerConfig:
    """Configuration data for the save manager."""
    username: str
    main_save_path: Path
    backup_directory: Path
    local_backup_directory: Path
