# Implementation Plan: Scumgenics Save Manager

## Overview

This implementation plan breaks down the Scumgenics save manager into discrete coding tasks following a layered architecture approach. The implementation progresses from foundational components (domain layer) through application logic to the presentation layer, with property-based tests and unit tests integrated throughout to validate correctness early.

## Tasks

- [x] 1. Set up project structure and dependencies
  - Create directory structure: `src/`, `tests/`, `backups/`
  - Create `requirements.txt` with dependencies: PyQt6, pytest, pytest-qt, pytest-mock, hypothesis, coverage
  - Create `src/__init__.py` and `tests/__init__.py`
  - Set up basic logging configuration
  - _Requirements: 1.2, 9.1, 9.3_

- [x] 2. Implement domain layer - PathBuilder
  - [x] 2.1 Create PathBuilder class with path construction methods
    - Implement `build_main_save_path(username)` using template
    - Implement `build_backup_directory_path(username)`
    - Implement `build_backup_filename(timestamp)` with format `steamcampaign01_YYYY-MM-DD_HH-MM.savbackup`
    - Implement `parse_backup_timestamp(filename)` to extract datetime from filename
    - Define constants: `GAME_DIRECTORY_TEMPLATE`, `MAIN_SAVE_FILENAME`, `BACKUP_SUBDIRECTORY`, `BACKUP_FILENAME_PATTERN`
    - _Requirements: 2.2, 2.3, 3.1, 4.1, 7.4_

  - [ ]* 2.2 Write property test for PathBuilder
    - **Property 1: Dynamic Path Construction**
    - **Validates: Requirements 2.2, 2.3, 3.1**
    - Generate random valid Windows usernames, verify paths follow template and differ per username

  - [ ]* 2.3 Write unit tests for PathBuilder
    - Test specific username examples
    - Test backup filename format and timestamp parsing
    - Test edge cases: special characters, long usernames
    - _Requirements: 2.2, 2.3, 3.1, 4.1_

- [x] 3. Implement domain layer - FileOperations
  - [x] 3.1 Create FileOperations class with file system methods
    - Implement `delete_file(path)` returning Result
    - Implement `copy_file(source, destination)` returning Result
    - Implement `rename_file(old_path, new_path)` returning Result
    - Implement `list_files(directory, pattern)` returning List[Path]
    - Implement `ensure_directory_exists(path)` returning Result
    - Implement `file_exists(path)` returning bool
    - Add error handling for FileNotFoundError, PermissionError, OSError
    - _Requirements: 3.3, 6.1, 6.2, 6.3, 7.3, 8.1, 8.2, 8.3_

  - [ ]* 3.2 Write unit tests for FileOperations
    - Test file operations with mock file system
    - Test error conditions: file not found, permission denied, I/O errors
    - Test directory creation
    - _Requirements: 8.1, 8.2, 8.3, 8.4_

- [x] 4. Implement data models
  - [x] 4.1 Create Result dataclass
    - Implement `Result` with `success`, `message`, `error_details` fields
    - Implement `Result.ok(message)` factory method
    - Implement `Result.error(message, details)` factory method
    - _Requirements: 6.4, 6.5, 7.5, 7.6_

  - [x] 4.2 Create BackupInfo dataclass
    - Implement `BackupInfo` with `filename`, `full_path`, `timestamp`, `size_bytes` fields
    - Implement `display_name()` method returning formatted string
    - _Requirements: 4.2, 4.3_

  - [x] 4.3 Create SaveManagerConfig dataclass
    - Implement `SaveManagerConfig` with `username`, `main_save_path`, `backup_directory`, `local_backup_directory` fields
    - _Requirements: 2.2, 3.1_

- [x] 5. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [x] 6. Implement application layer - SaveManager
  - [x] 6.1 Create SaveManager class initialization
    - Implement `__init__()` to detect username using `os.getlogin()` or `os.environ['USERNAME']`
    - Initialize SaveManagerConfig with constructed paths
    - Create PathBuilder and FileOperations instances
    - _Requirements: 2.1, 2.2, 2.3_

  - [ ]* 6.2 Write property test for SaveManager initialization
    - **Property 2: Main Save Existence Verification**
    - **Validates: Requirements 3.3**
    - Verify existence check occurs before operations

  - [ ]* 6.3 Write property test for cross-user portability
    - **Property 12: Cross-User Portability**
    - **Validates: Requirements 9.4**
    - Generate random username pairs, verify application operates correctly for both

  - [x] 6.4 Implement SaveManager backup listing methods
    - Implement `get_main_save_path()` returning Path
    - Implement `get_backup_directory()` returning Path
    - Implement `get_local_backup_directory()` returning Path
    - Implement `list_backups()` to scan directories, parse filenames, create BackupInfo objects, sort by timestamp descending
    - Implement `verify_main_save_exists()` returning bool
    - _Requirements: 3.1, 3.3, 4.1, 4.2, 4.3, 4.4_

  - [ ]* 6.5 Write property test for backup pattern filtering
    - **Property 3: Backup Pattern Filtering**
    - **Validates: Requirements 4.1**
    - Generate random directory contents, verify only pattern-matching files returned

  - [ ]* 6.6 Write property test for backup timestamp sorting
    - **Property 5: Backup Timestamp Sorting**
    - **Validates: Requirements 4.3**
    - Generate random backup file lists, verify descending timestamp order

  - [x] 6.7 Implement SaveManager restore operation
    - Implement `restore_backup(backup_filename)` method
    - Verify main save exists before deletion
    - Verify backup file is readable before deletion
    - Delete main save using FileOperations
    - Copy backup to game directory using FileOperations
    - Rename copied file to `steamcampaign01.sav` using FileOperations
    - Return Result with success/error message including file paths
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 8.4_

  - [ ]* 6.8 Write property test for restore operation sequence
    - **Property 7: Restore Operation Sequence**
    - **Validates: Requirements 6.1, 6.2, 6.3**
    - Generate random backup files, verify delete-copy-rename sequence and content preservation

  - [ ]* 6.9 Write unit tests for restore operation
    - Test successful restore with mock file system
    - Test restore failure scenarios: main save missing, backup missing, permission errors
    - Verify error messages include file paths
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 8.4_

  - [x] 6.10 Implement SaveManager local backup creation
    - Implement `create_local_backup()` method
    - Verify main save exists
    - Ensure local backup directory exists using FileOperations
    - Generate timestamped filename using PathBuilder
    - Copy main save to local backup directory using FileOperations
    - Return Result with success/error message
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5, 7.6_

  - [ ]* 6.11 Write property test for local backup creation
    - **Property 10: Local Backup Creation with Timestamp**
    - **Validates: Requirements 7.2, 7.4**
    - Generate random backup creation requests, verify filename format and timestamp accuracy

  - [ ]* 6.12 Write property test for directory creation on demand
    - **Property 11: Directory Creation on Demand**
    - **Validates: Requirements 7.3**
    - Generate random backup operations with non-existent directories, verify directory exists after operation

  - [ ]* 6.13 Write unit tests for local backup creation
    - Test successful backup creation with mock file system
    - Test failure scenarios: main save missing, permission errors, disk full
    - Verify directory creation when missing
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5, 7.6_

- [x] 7. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [x] 8. Implement presentation layer - MainWindow
  - [x] 8.1 Create MainWindow class with basic UI structure
    - Implement `__init__()` to set window title "Scumgenics"
    - Create QListWidget for backup list display
    - Create QPushButton for "Restore" (initially disabled)
    - Create QPushButton for "Create Local Backup"
    - Create QLabel for status messages
    - Set up basic layout using QVBoxLayout
    - _Requirements: 1.1, 1.2, 4.2, 5.1, 7.1_

  - [ ]* 8.2 Write unit test for MainWindow initialization
    - Test window title is "Scumgenics"
    - Test UI widgets exist
    - Test restore button initially disabled
    - _Requirements: 1.1, 5.3_

  - [x] 8.3 Implement MainWindow backup display methods
    - Implement `display_backups(backups)` to populate QListWidget with BackupInfo display names
    - Implement `display_error(message)` to show QMessageBox error dialog
    - Implement `display_success(message)` to show QMessageBox success dialog
    - Implement `get_selected_backup()` to return selected backup filename or None
    - _Requirements: 4.2, 6.4, 6.5, 7.5, 7.6_

  - [ ]* 8.4 Write property test for backup list display completeness
    - **Property 4: Backup List Display Completeness**
    - **Validates: Requirements 4.2**
    - Generate random backup file lists, verify all filenames appear in UI

  - [ ]* 8.5 Write unit tests for display methods
    - Test backup list population with mock BackupInfo objects
    - Test error and success message dialogs
    - Test empty backup list displays correctly
    - _Requirements: 4.2, 4.4, 6.4, 6.5_

  - [x] 8.6 Implement MainWindow event handlers and button state management
    - Connect QListWidget selection changed signal to update restore button state
    - Implement restore button state logic: enabled when backup selected, disabled otherwise
    - Implement `on_restore_clicked()` handler to call SaveManager.restore_backup()
    - Implement `on_create_backup_clicked()` handler to call SaveManager.create_local_backup()
    - Display success/error messages based on Result
    - Refresh backup list after successful operations
    - _Requirements: 5.1, 5.2, 5.3, 6.4, 6.5, 7.5, 7.6_

  - [ ]* 8.7 Write property test for restore button state consistency
    - **Property 6: Restore Button State Consistency**
    - **Validates: Requirements 5.2, 5.3**
    - Generate random UI selection states, verify button enabled state matches selection state

  - [ ]* 8.8 Write property test for operation success feedback
    - **Property 8: Operation Success Feedback**
    - **Validates: Requirements 6.4, 7.5**
    - Generate random successful operations, verify success message displayed

  - [ ]* 8.9 Write property test for operation failure feedback
    - **Property 9: Operation Failure Feedback**
    - **Validates: Requirements 6.5, 7.6, 8.1, 8.2, 8.3, 8.4**
    - Generate random failure scenarios, verify error message includes reason and path

  - [ ]* 8.10 Write unit tests for event handlers
    - Test restore button state changes with selection
    - Test restore operation with mock SaveManager
    - Test backup creation with mock SaveManager
    - Test UI updates after operations
    - _Requirements: 5.1, 5.2, 5.3, 6.4, 6.5, 7.5, 7.6_

- [x] 9. Create application entry point
  - [x] 9.1 Create main.py with application startup
    - Import PyQt6.QtWidgets.QApplication
    - Create SaveManager instance
    - Create MainWindow instance
    - Initialize MainWindow with SaveManager
    - Load and display initial backup list
    - Handle initialization errors (username detection, main save missing)
    - Start Qt event loop with sys.exit(app.exec())
    - _Requirements: 1.1, 1.2, 1.3, 2.1, 3.2, 9.1_

  - [ ]* 9.2 Write integration test for application startup
    - Test application launches successfully
    - Test error handling when main save missing
    - Test backup list loads on startup
    - _Requirements: 1.1, 1.3, 3.2, 4.2_

- [x] 10. Implement logging system
  - [x] 10.1 Add logging to all error paths
    - Configure logging to write to `scumgenics.log` in application directory
    - Log all exceptions with timestamp, operation, file paths, exception details
    - Log username detection and path construction
    - Log all file operations (delete, copy, rename)
    - _Requirements: 8.1, 8.2, 8.3, 8.4_

- [x] 11. Final checkpoint - Ensure all tests pass
  - Run full test suite with coverage report
  - Verify coverage >90%
  - Ensure all tests pass, ask the user if questions arise.

- [x] 12. Create distribution package
  - [x] 12.1 Create README.md with installation and usage instructions
    - Document Python version requirement
    - Document installation steps: `pip install -r requirements.txt`
    - Document how to run: `python main.py`
    - Document backup directory locations
    - Include troubleshooting section for common errors
    - _Requirements: 9.1, 9.3, 9.4_

  - [x] 12.2 Test on clean Windows environment
    - Verify application runs without pre-configuration
    - Test with different Windows usernames
    - Verify all dependencies install correctly
    - _Requirements: 9.2, 9.4_

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Property tests use Hypothesis with minimum 100 iterations
- All property tests include feature and property number comments
- Checkpoints ensure incremental validation throughout implementation
- The application uses PyQt6 for GUI, pytest for testing, and Hypothesis for property-based testing
- Mock file system operations in tests to avoid modifying real files during testing
