"""SaveManager class for orchestrating save file operations."""
import os
import logging
from pathlib import Path
from typing import List, Optional
from datetime import datetime

from src.save_manager_config import SaveManagerConfig
from src.path_builder import PathBuilder
from src.file_operations import FileOperations
from src.backup_info import BackupInfo
from src.result import Result

logger = logging.getLogger("scumgenics.save_manager")


class SaveManager:
    """Orchestrates save file operations and business logic."""
    
    def __init__(self):
        """Initialize save manager with path configuration."""
        # Detect username using os.getlogin() or os.environ['USERNAME']
        username = self._detect_username()
        logger.info(f"Detected username: {username}")
        
        # Construct paths using PathBuilder
        main_save_path = PathBuilder.build_main_save_path(username)
        backup_directory = PathBuilder.build_backup_directory_path(username)
        local_backup_directory = Path("./backups")
        
        logger.info(f"Main save path: {main_save_path}")
        logger.info(f"Backup directory: {backup_directory}")
        logger.info(f"Local backup directory: {local_backup_directory}")
        
        # Initialize configuration
        self.config = SaveManagerConfig(
            username=username,
            main_save_path=main_save_path,
            backup_directory=backup_directory,
            local_backup_directory=local_backup_directory
        )
        
        # Create PathBuilder and FileOperations instances
        self.path_builder = PathBuilder()
        self.file_ops = FileOperations()
    
    def _detect_username(self) -> str:
        """Detect and return the current Windows username from the user profile path.
        
        Returns:
            The current Windows username (extracted from USERPROFILE path)
            
        Raises:
            RuntimeError: If username cannot be detected
        """
        # Use USERPROFILE to get the actual profile folder name
        # This handles cases where USERNAME env var differs from the profile folder
        # (e.g., display name vs actual profile folder name)
        userprofile = os.environ.get('USERPROFILE')
        if userprofile:
            username = Path(userprofile).name
            logger.debug(f"Username detected from USERPROFILE path: {username}")
            return username
        
        # Fall back to os.getlogin()
        try:
            username = os.getlogin()
            logger.debug(f"Username detected via os.getlogin(): {username}")
            return username
        except (OSError, AttributeError) as e:
            logger.warning(f"os.getlogin() failed: {str(e)}, trying USERNAME environment variable")
            # Last resort: environment variable
            username = os.environ.get('USERNAME')
            if username:
                logger.debug(f"Username detected via USERNAME environment variable: {username}")
                return username
            logger.error("Failed to detect username via USERPROFILE, os.getlogin(), or USERNAME")
            raise RuntimeError("Unable to detect Windows username")

    def get_main_save_path(self) -> Path:
        """Return the path to the main save file.
        
        Returns:
            Path to the main save file
        """
        return self.config.main_save_path
    
    def get_backup_directory(self) -> Path:
        """Return the path to the backup directory.
        
        Returns:
            Path to the backup directory
        """
        return self.config.backup_directory
    
    def get_local_backup_directory(self) -> Path:
        """Return the path to the local backup directory.
        
        Returns:
            Path to the local backup directory
        """
        return self.config.local_backup_directory
    
    def list_backups(self) -> List[BackupInfo]:
        """Scan and return list of available backups, sorted by timestamp descending.
        
        Returns:
            List of BackupInfo objects sorted by timestamp (newest first)
        """
        logger.debug("Scanning for backup files")
        backups = []
        
        # Scan backup directory
        backup_files = self.file_ops.list_files(
            self.config.backup_directory,
            PathBuilder.BACKUP_FILENAME_PATTERN
        )
        logger.debug(f"Found {len(backup_files)} backup(s) in {self.config.backup_directory}")
        
        # Scan local backup directory
        local_backup_files = self.file_ops.list_files(
            self.config.local_backup_directory,
            PathBuilder.BACKUP_FILENAME_PATTERN
        )
        logger.debug(f"Found {len(local_backup_files)} local backup(s) in {self.config.local_backup_directory}")
        
        # Combine both lists
        all_backup_files = backup_files + local_backup_files
        
        # Parse each backup file and create BackupInfo objects
        for backup_path in all_backup_files:
            timestamp = PathBuilder.parse_backup_timestamp(backup_path.name)
            if timestamp:
                try:
                    size_bytes = backup_path.stat().st_size
                    backup_info = BackupInfo(
                        filename=backup_path.name,
                        full_path=backup_path,
                        timestamp=timestamp,
                        size_bytes=size_bytes
                    )
                    backups.append(backup_info)
                except OSError as e:
                    # Skip files that can't be accessed
                    logger.warning(f"Could not access backup file {backup_path}: {str(e)}")
                    continue
        
        # Sort by timestamp descending (newest first)
        backups.sort(key=lambda b: b.timestamp, reverse=True)
        logger.info(f"Total backups found: {len(backups)}")
        
        return backups
    
    def verify_main_save_exists(self) -> bool:
        """Check if the main save file exists.
        
        Returns:
            True if main save file exists, False otherwise
        """
        return self.file_ops.file_exists(self.config.main_save_path)

    def restore_backup(self, backup_filename: str) -> Result:
        """Restore a backup as the main save file.
        
        Args:
            backup_filename: Name of the backup file to restore
            
        Returns:
            Result indicating success or error with detailed message
        """
        logger.info(f"Starting restore operation for backup: {backup_filename}")
        
        # Verify main save exists before deletion
        if not self.verify_main_save_exists():
            logger.error(f"Restore failed: Main save file not found at {self.config.main_save_path}")
            return Result.error(
                "Restore failed: Main save file not found",
                f"File: {self.config.main_save_path}"
            )
        
        # Find the backup file (check both directories)
        backup_path = None
        
        # Check backup directory first
        potential_path = self.config.backup_directory / backup_filename
        if self.file_ops.file_exists(potential_path):
            backup_path = potential_path
            logger.debug(f"Found backup in game directory: {backup_path}")
        else:
            # Check local backup directory
            potential_path = self.config.local_backup_directory / backup_filename
            if self.file_ops.file_exists(potential_path):
                backup_path = potential_path
                logger.debug(f"Found backup in local directory: {backup_path}")
        
        if backup_path is None:
            logger.error(f"Restore failed: Backup file not found: {backup_filename}")
            return Result.error(
                "Restore failed: Backup file not found",
                f"File: {backup_filename}"
            )
        
        # Verify backup file is readable before deletion
        try:
            with open(backup_path, 'rb') as f:
                f.read(1)  # Try to read one byte to verify readability
            logger.debug(f"Verified backup file is readable: {backup_path}")
        except (OSError, PermissionError) as e:
            logger.error(f"Restore failed: Backup file not readable: {backup_path}, error: {str(e)}", exc_info=True)
            return Result.error(
                "Restore failed: Backup file is not readable",
                f"File: {backup_path}\n{str(e)}"
            )
        
        # Delete main save using FileOperations
        logger.info(f"Deleting main save: {self.config.main_save_path}")
        delete_result = self.file_ops.delete_file(self.config.main_save_path)
        if not delete_result.success:
            logger.error(f"Restore failed: Could not delete main save: {delete_result.error_details}")
            return delete_result
        
        # Copy backup to game directory using FileOperations
        game_directory = self.config.main_save_path.parent
        temp_copy_path = game_directory / backup_filename
        
        logger.info(f"Copying backup to game directory: {backup_path} -> {temp_copy_path}")
        copy_result = self.file_ops.copy_file(backup_path, temp_copy_path)
        if not copy_result.success:
            logger.error(f"Restore failed: Could not copy backup file: {copy_result.error_details}")
            return Result.error(
                "Restore failed: Could not copy backup file",
                f"Main save was deleted but restoration failed.\n"
                f"Please manually copy: {backup_path}\n"
                f"To: {self.config.main_save_path}\n"
                f"Error: {copy_result.error_details}"
            )
        
        # Rename copied file to steamcampaign01.sav using FileOperations
        logger.info(f"Renaming copied file: {temp_copy_path} -> {self.config.main_save_path}")
        rename_result = self.file_ops.rename_file(temp_copy_path, self.config.main_save_path)
        if not rename_result.success:
            logger.error(f"Restore failed: Could not rename copied file: {rename_result.error_details}")
            return Result.error(
                "Restore failed: Could not rename copied file",
                f"Backup was copied to: {temp_copy_path}\n"
                f"Please manually rename to: {self.config.main_save_path}\n"
                f"Error: {rename_result.error_details}"
            )
        
        # Return success with file paths
        logger.info(f"Restore completed successfully: {backup_filename} -> {self.config.main_save_path}")
        return Result.ok(
            f"Backup restored successfully: {backup_filename} -> {self.config.main_save_path}"
        )

    def create_local_backup(self) -> Result:
        """Create a timestamped backup in the local directory.
        
        Returns:
            Result indicating success or error with detailed message
        """
        logger.info("Starting local backup creation")
        
        # Verify main save exists
        if not self.verify_main_save_exists():
            logger.error(f"Backup creation failed: Main save file not found at {self.config.main_save_path}")
            return Result.error(
                "Backup creation failed: Main save file not found",
                f"File: {self.config.main_save_path}"
            )
        
        # Ensure local backup directory exists using FileOperations
        logger.debug(f"Ensuring local backup directory exists: {self.config.local_backup_directory}")
        ensure_result = self.file_ops.ensure_directory_exists(self.config.local_backup_directory)
        if not ensure_result.success:
            logger.error(f"Backup creation failed: Could not create directory: {ensure_result.error_details}")
            return ensure_result
        
        # Generate timestamped filename using PathBuilder
        timestamp = datetime.now()
        backup_filename = PathBuilder.build_backup_filename(timestamp)
        backup_path = self.config.local_backup_directory / backup_filename
        
        logger.info(f"Creating backup: {self.config.main_save_path} -> {backup_path}")
        
        # Copy main save to local backup directory using FileOperations
        copy_result = self.file_ops.copy_file(self.config.main_save_path, backup_path)
        if not copy_result.success:
            logger.error(f"Backup creation failed: Could not copy file: {copy_result.error_details}")
            return copy_result
        
        # Return success message
        logger.info(f"Local backup created successfully: {backup_path}")
        return Result.ok(
            f"Local backup created successfully: {backup_path}"
        )
