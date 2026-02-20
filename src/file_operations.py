"""FileOperations class for handling file system operations with error handling."""
import shutil
import re
import logging
from pathlib import Path
from typing import List
from src.result import Result

logger = logging.getLogger("scumgenics.file_operations")


class FileOperations:
    """Handles low-level file system operations with error handling."""
    
    @staticmethod
    def delete_file(path: Path) -> Result:
        """
        Delete a file.
        
        Args:
            path: Path to the file to delete
            
        Returns:
            Result indicating success or error
        """
        try:
            logger.debug(f"Deleting file: {path}")
            path.unlink()
            logger.info(f"File deleted successfully: {path}")
            return Result.ok(f"File deleted successfully: {path}")
        except FileNotFoundError:
            logger.error(f"Delete failed: File not found: {path}")
            return Result.error(
                f"Delete failed: File not found",
                f"File: {path}"
            )
        except PermissionError:
            logger.error(f"Delete failed: Access denied: {path}")
            return Result.error(
                f"Delete failed: Access denied",
                f"File: {path}\nPlease check file permissions."
            )
        except OSError as e:
            logger.error(f"Delete failed: I/O error for {path}: {str(e)}", exc_info=True)
            return Result.error(
                f"Delete failed: I/O error",
                f"File: {path}\n{str(e)}"
            )
    
    @staticmethod
    def copy_file(source: Path, destination: Path) -> Result:
        """
        Copy a file from source to destination.
        
        Args:
            source: Path to the source file
            destination: Path to the destination file
            
        Returns:
            Result indicating success or error
        """
        try:
            logger.debug(f"Copying file: {source} -> {destination}")
            shutil.copy2(source, destination)
            logger.info(f"File copied successfully: {source} -> {destination}")
            return Result.ok(f"File copied successfully: {source} -> {destination}")
        except FileNotFoundError:
            logger.error(f"Copy failed: File not found: {source}")
            return Result.error(
                f"Copy failed: File not found",
                f"File: {source}"
            )
        except PermissionError:
            logger.error(f"Copy failed: Access denied: {source} or {destination}")
            return Result.error(
                f"Copy failed: Access denied",
                f"File: {source} or {destination}\nPlease check file permissions."
            )
        except OSError as e:
            logger.error(f"Copy failed: I/O error for {source} -> {destination}: {str(e)}", exc_info=True)
            return Result.error(
                f"Copy failed: I/O error",
                f"File: {source} -> {destination}\n{str(e)}"
            )

    @staticmethod
    def rename_file(old_path: Path, new_path: Path) -> Result:
        """
        Rename a file.
        
        Args:
            old_path: Current path to the file
            new_path: New path for the file
            
        Returns:
            Result indicating success or error
        """
        try:
            logger.debug(f"Renaming file: {old_path} -> {new_path}")
            old_path.rename(new_path)
            logger.info(f"File renamed successfully: {old_path} -> {new_path}")
            return Result.ok(f"File renamed successfully: {old_path} -> {new_path}")
        except FileNotFoundError:
            logger.error(f"Rename failed: File not found: {old_path}")
            return Result.error(
                f"Rename failed: File not found",
                f"File: {old_path}"
            )
        except PermissionError:
            logger.error(f"Rename failed: Access denied: {old_path} or {new_path}")
            return Result.error(
                f"Rename failed: Access denied",
                f"File: {old_path} or {new_path}\nPlease check file permissions."
            )
        except OSError as e:
            logger.error(f"Rename failed: I/O error for {old_path} -> {new_path}: {str(e)}", exc_info=True)
            return Result.error(
                f"Rename failed: I/O error",
                f"File: {old_path} -> {new_path}\n{str(e)}"
            )
    
    @staticmethod
    def list_files(directory: Path, pattern: str) -> List[Path]:
        """
        List files in directory matching pattern.
        
        Args:
            directory: Path to the directory to scan
            pattern: Regex pattern to match filenames
            
        Returns:
            List of Path objects matching the pattern
        """
        try:
            if not directory.exists():
                logger.debug(f"Directory does not exist: {directory}")
                return []
            
            regex = re.compile(pattern)
            matching_files = []
            
            for file_path in directory.iterdir():
                if file_path.is_file() and regex.match(file_path.name):
                    matching_files.append(file_path)
            
            logger.debug(f"Found {len(matching_files)} file(s) matching pattern in {directory}")
            return matching_files
        except PermissionError as e:
            logger.error(f"List files failed: Access denied for directory {directory}: {str(e)}")
            # Return empty list on error to avoid breaking the application
            return []
        except OSError as e:
            logger.error(f"List files failed: I/O error for directory {directory}: {str(e)}", exc_info=True)
            # Return empty list on error to avoid breaking the application
            return []
    
    @staticmethod
    def ensure_directory_exists(path: Path) -> Result:
        """
        Create directory if it doesn't exist.
        
        Args:
            path: Path to the directory
            
        Returns:
            Result indicating success or error
        """
        try:
            logger.debug(f"Ensuring directory exists: {path}")
            path.mkdir(parents=True, exist_ok=True)
            logger.info(f"Directory ready: {path}")
            return Result.ok(f"Directory ready: {path}")
        except PermissionError:
            logger.error(f"Directory creation failed: Access denied for {path}")
            return Result.error(
                f"Directory creation failed: Access denied",
                f"File: {path}\nPlease check file permissions."
            )
        except OSError as e:
            logger.error(f"Directory creation failed: I/O error for {path}: {str(e)}", exc_info=True)
            return Result.error(
                f"Directory creation failed: I/O error",
                f"File: {path}\n{str(e)}"
            )
    
    @staticmethod
    def file_exists(path: Path) -> bool:
        """
        Check if file exists.
        
        Args:
            path: Path to the file
            
        Returns:
            True if file exists, False otherwise
        """
        return path.exists() and path.is_file()
