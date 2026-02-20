"""Settings management for persistent configuration."""
import json
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger("scumgenics.settings")


class Settings:
    """Manages persistent application settings."""
    
    SETTINGS_FILE = Path("settings.json")
    
    @staticmethod
    def load_custom_save_folder() -> Optional[Path]:
        """Load custom save folder path from settings file.
        
        Returns:
            Path to custom save folder or None if not set
        """
        if not Settings.SETTINGS_FILE.exists():
            return None
        
        try:
            with open(Settings.SETTINGS_FILE, 'r') as f:
                data = json.load(f)
                custom_path = data.get('custom_save_folder')
                if custom_path:
                    logger.info(f"Loaded custom save folder: {custom_path}")
                    return Path(custom_path)
        except Exception as e:
            logger.error(f"Failed to load settings: {e}")
        
        return None
    
    @staticmethod
    def load_game_executable_path() -> Optional[Path]:
        """Load game executable path from settings file.
        
        Returns:
            Path to game executable or None if not set
        """
        if not Settings.SETTINGS_FILE.exists():
            return None
        
        try:
            with open(Settings.SETTINGS_FILE, 'r') as f:
                data = json.load(f)
                exe_path = data.get('game_executable_path')
                if exe_path:
                    logger.info(f"Loaded game executable path: {exe_path}")
                    return Path(exe_path)
        except Exception as e:
            logger.error(f"Failed to load settings: {e}")
        
        return None
    
    @staticmethod
    def save_custom_save_folder(path: Optional[Path]) -> None:
        """Save custom save folder path to settings file.
        
        Args:
            path: Path to custom save folder or None to clear
        """
        try:
            data = {}
            if Settings.SETTINGS_FILE.exists():
                with open(Settings.SETTINGS_FILE, 'r') as f:
                    data = json.load(f)
            
            if path:
                data['custom_save_folder'] = str(path)
                logger.info(f"Saved custom save folder: {path}")
            else:
                data.pop('custom_save_folder', None)
                logger.info("Cleared custom save folder")
            
            with open(Settings.SETTINGS_FILE, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save settings: {e}")
    
    @staticmethod
    def save_game_executable_path(path: Optional[Path]) -> None:
        """Save game executable path to settings file.
        
        Args:
            path: Path to game executable or None to clear
        """
        try:
            data = {}
            if Settings.SETTINGS_FILE.exists():
                with open(Settings.SETTINGS_FILE, 'r') as f:
                    data = json.load(f)
            
            if path:
                data['game_executable_path'] = str(path)
                logger.info(f"Saved game executable path: {path}")
            else:
                data.pop('game_executable_path', None)
                logger.info("Cleared game executable path")
            
            with open(Settings.SETTINGS_FILE, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save settings: {e}")
