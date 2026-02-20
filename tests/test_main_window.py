"""Unit tests for MainWindow class."""
import pytest
from unittest.mock import Mock, MagicMock
from PyQt6.QtWidgets import QApplication
from datetime import datetime
from pathlib import Path

from src.main_window import MainWindow
from src.backup_info import BackupInfo
from src.result import Result


@pytest.fixture
def qapp():
    """Create QApplication instance for tests."""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


@pytest.fixture
def mock_save_manager():
    """Create a mock SaveManager instance."""
    manager = Mock()
    manager.list_backups.return_value = []
    return manager


@pytest.fixture
def main_window(qapp, mock_save_manager):
    """Create MainWindow instance for tests."""
    window = MainWindow(mock_save_manager)
    return window


def test_window_title(main_window):
    """Test window title is 'Scumgenics'."""
    assert main_window.windowTitle() == "Scumgenics"


def test_restore_button_initially_disabled(main_window):
    """Test restore button is initially disabled."""
    assert not main_window.restore_button.isEnabled()


def test_ui_widgets_exist(main_window):
    """Test all required UI widgets exist."""
    assert main_window.backup_list is not None
    assert main_window.restore_button is not None
    assert main_window.create_backup_button is not None
    assert main_window.status_label is not None


def test_display_backups(main_window):
    """Test backup list population with BackupInfo objects."""
    backups = [
        BackupInfo(
            filename="steamcampaign01_2024-01-15_14-30.savbackup",
            full_path=Path("/test/path1"),
            timestamp=datetime(2024, 1, 15, 14, 30),
            size_bytes=1024
        ),
        BackupInfo(
            filename="steamcampaign01_2024-01-14_10-00.savbackup",
            full_path=Path("/test/path2"),
            timestamp=datetime(2024, 1, 14, 10, 0),
            size_bytes=2048
        )
    ]
    
    main_window.display_backups(backups)
    
    assert main_window.backup_list.count() == 2
    assert main_window.backup_list.item(0).text() == "2024-01-15 14:30 (1 KB)"
    assert main_window.backup_list.item(1).text() == "2024-01-14 10:00 (2 KB)"


def test_restore_button_enabled_when_backup_selected(main_window):
    """Test restore button state changes with selection."""
    backups = [
        BackupInfo(
            filename="steamcampaign01_2024-01-15_14-30.savbackup",
            full_path=Path("/test/path"),
            timestamp=datetime(2024, 1, 15, 14, 30),
            size_bytes=1024
        )
    ]
    
    main_window.display_backups(backups)
    
    # Initially disabled
    assert not main_window.restore_button.isEnabled()
    
    # Select an item
    main_window.backup_list.setCurrentRow(0)
    
    # Should be enabled now
    assert main_window.restore_button.isEnabled()
    
    # Clear selection
    main_window.backup_list.clearSelection()
    
    # Should be disabled again
    assert not main_window.restore_button.isEnabled()


def test_get_selected_backup_returns_none_when_no_selection(main_window, mock_save_manager):
    """Test get_selected_backup returns None when no selection."""
    mock_save_manager.list_backups.return_value = []
    assert main_window.get_selected_backup() is None


def test_get_selected_backup_returns_filename(main_window, mock_save_manager):
    """Test get_selected_backup returns correct filename."""
    backups = [
        BackupInfo(
            filename="steamcampaign01_2024-01-15_14-30.savbackup",
            full_path=Path("/test/path"),
            timestamp=datetime(2024, 1, 15, 14, 30),
            size_bytes=1024
        )
    ]
    
    mock_save_manager.list_backups.return_value = backups
    main_window.display_backups(backups)
    main_window.backup_list.setCurrentRow(0)
    
    assert main_window.get_selected_backup() == "steamcampaign01_2024-01-15_14-30.savbackup"


def test_on_restore_clicked_success(main_window, mock_save_manager, monkeypatch):
    """Test restore operation with successful result."""
    backups = [
        BackupInfo(
            filename="steamcampaign01_2024-01-15_14-30.savbackup",
            full_path=Path("/test/path"),
            timestamp=datetime(2024, 1, 15, 14, 30),
            size_bytes=1024
        )
    ]
    
    mock_save_manager.list_backups.return_value = backups
    mock_save_manager.restore_backup.return_value = Result.ok("Backup restored successfully")
    
    # Mock display methods
    main_window.display_success = Mock()
    main_window.display_error = Mock()
    
    main_window.display_backups(backups)
    main_window.backup_list.setCurrentRow(0)
    main_window.on_restore_clicked()
    
    mock_save_manager.restore_backup.assert_called_once_with("steamcampaign01_2024-01-15_14-30.savbackup")
    main_window.display_success.assert_called_once()
    main_window.display_error.assert_not_called()


def test_on_restore_clicked_error(main_window, mock_save_manager):
    """Test restore operation with error result."""
    backups = [
        BackupInfo(
            filename="steamcampaign01_2024-01-15_14-30.savbackup",
            full_path=Path("/test/path"),
            timestamp=datetime(2024, 1, 15, 14, 30),
            size_bytes=1024
        )
    ]
    
    mock_save_manager.list_backups.return_value = backups
    mock_save_manager.restore_backup.return_value = Result.error(
        "Restore failed",
        "File not found"
    )
    
    # Mock display methods
    main_window.display_success = Mock()
    main_window.display_error = Mock()
    
    main_window.display_backups(backups)
    main_window.backup_list.setCurrentRow(0)
    main_window.on_restore_clicked()
    
    main_window.display_error.assert_called_once()
    main_window.display_success.assert_not_called()


def test_on_create_backup_clicked_success(main_window, mock_save_manager):
    """Test backup creation with successful result."""
    mock_save_manager.create_local_backup.return_value = Result.ok("Backup created successfully")
    mock_save_manager.list_backups.return_value = []
    
    # Mock display methods
    main_window.display_success = Mock()
    main_window.display_error = Mock()
    
    main_window.on_create_backup_clicked()
    
    mock_save_manager.create_local_backup.assert_called_once()
    main_window.display_success.assert_called_once()
    main_window.display_error.assert_not_called()


def test_on_create_backup_clicked_error(main_window, mock_save_manager):
    """Test backup creation with error result."""
    mock_save_manager.create_local_backup.return_value = Result.error(
        "Backup creation failed",
        "Main save not found"
    )
    
    # Mock display methods
    main_window.display_success = Mock()
    main_window.display_error = Mock()
    
    main_window.on_create_backup_clicked()
    
    main_window.display_error.assert_called_once()
    main_window.display_success.assert_not_called()


def test_empty_backup_list_displays_correctly(main_window):
    """Test empty backup list displays correctly."""
    main_window.display_backups([])
    assert main_window.backup_list.count() == 0
