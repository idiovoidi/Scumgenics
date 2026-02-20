"""Integration tests for logging functionality."""
import logging
import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

from src.save_manager import SaveManager
from src.file_operations import FileOperations
from src.logging_config import setup_logging

# Try to import pytest-qt, skip GUI tests if not available
try:
    from pytestqt.plugin import QtBot
    from src.main_window import MainWindow
    PYTEST_QT_AVAILABLE = True
except ImportError:
    PYTEST_QT_AVAILABLE = False


@pytest.fixture
def mock_logger():
    """Create a mock logger for testing."""
    logger = Mock(spec=logging.Logger)
    return logger


class TestLoggingIntegration:
    """Test that logging is properly integrated into all components."""
    
    def test_save_manager_logs_username_detection(self, mock_logger):
        """Test that SaveManager logs username detection."""
        with patch('src.save_manager.logger', mock_logger):
            with patch('os.getlogin', return_value='testuser'):
                save_manager = SaveManager()
                
                # Verify username detection was logged
                mock_logger.info.assert_any_call("Detected username: testuser")
    
    def test_save_manager_logs_path_construction(self, mock_logger):
        """Test that SaveManager logs path construction."""
        with patch('src.save_manager.logger', mock_logger):
            with patch('os.getlogin', return_value='testuser'):
                save_manager = SaveManager()
                
                # Verify paths were logged
                assert any('Main save path:' in str(call) for call in mock_logger.info.call_args_list)
                assert any('Backup directory:' in str(call) for call in mock_logger.info.call_args_list)
                assert any('Local backup directory:' in str(call) for call in mock_logger.info.call_args_list)
    
    def test_save_manager_logs_username_detection_failure(self, mock_logger):
        """Test that SaveManager logs username detection failure."""
        with patch('src.save_manager.logger', mock_logger):
            with patch('os.getlogin', side_effect=OSError("No login")):
                with patch.dict('os.environ', {}, clear=True):
                    with pytest.raises(RuntimeError):
                        SaveManager()
                    
                    # Verify error was logged
                    mock_logger.error.assert_called()
    
    def test_file_operations_logs_delete_success(self, mock_logger, tmp_path):
        """Test that FileOperations logs successful delete."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("test")
        
        with patch('src.file_operations.logger', mock_logger):
            result = FileOperations.delete_file(test_file)
            
            assert result.success
            mock_logger.info.assert_called()
    
    def test_file_operations_logs_delete_error(self, mock_logger, tmp_path):
        """Test that FileOperations logs delete errors."""
        test_file = tmp_path / "nonexistent.txt"
        
        with patch('src.file_operations.logger', mock_logger):
            result = FileOperations.delete_file(test_file)
            
            assert not result.success
            mock_logger.error.assert_called()
    
    def test_file_operations_logs_copy_success(self, mock_logger, tmp_path):
        """Test that FileOperations logs successful copy."""
        source = tmp_path / "source.txt"
        dest = tmp_path / "dest.txt"
        source.write_text("test")
        
        with patch('src.file_operations.logger', mock_logger):
            result = FileOperations.copy_file(source, dest)
            
            assert result.success
            mock_logger.info.assert_called()
    
    def test_file_operations_logs_copy_error(self, mock_logger, tmp_path):
        """Test that FileOperations logs copy errors."""
        source = tmp_path / "nonexistent.txt"
        dest = tmp_path / "dest.txt"
        
        with patch('src.file_operations.logger', mock_logger):
            result = FileOperations.copy_file(source, dest)
            
            assert not result.success
            mock_logger.error.assert_called()
    
    def test_file_operations_logs_rename_success(self, mock_logger, tmp_path):
        """Test that FileOperations logs successful rename."""
        old_path = tmp_path / "old.txt"
        new_path = tmp_path / "new.txt"
        old_path.write_text("test")
        
        with patch('src.file_operations.logger', mock_logger):
            result = FileOperations.rename_file(old_path, new_path)
            
            assert result.success
            mock_logger.info.assert_called()
    
    def test_file_operations_logs_rename_error(self, mock_logger, tmp_path):
        """Test that FileOperations logs rename errors."""
        old_path = tmp_path / "nonexistent.txt"
        new_path = tmp_path / "new.txt"
        
        with patch('src.file_operations.logger', mock_logger):
            result = FileOperations.rename_file(old_path, new_path)
            
            assert not result.success
            mock_logger.error.assert_called()
    
    def test_file_operations_logs_ensure_directory_success(self, mock_logger, tmp_path):
        """Test that FileOperations logs successful directory creation."""
        test_dir = tmp_path / "test_dir"
        
        with patch('src.file_operations.logger', mock_logger):
            result = FileOperations.ensure_directory_exists(test_dir)
            
            assert result.success
            mock_logger.info.assert_called()
    
    def test_save_manager_logs_restore_operation(self, mock_logger, tmp_path):
        """Test that SaveManager logs restore operations."""
        with patch('src.save_manager.logger', mock_logger):
            with patch('os.getlogin', return_value='testuser'):
                save_manager = SaveManager()
                
                # Mock file operations
                save_manager.file_ops.file_exists = Mock(return_value=True)
                
                # Create mock backup file
                backup_file = tmp_path / "backup.savbackup"
                backup_file.write_text("test")
                
                # Mock the backup directory to return our test file
                save_manager.config.backup_directory = tmp_path
                
                # Attempt restore (will fail but should log)
                result = save_manager.restore_backup("backup.savbackup")
                
                # Verify restore operation was logged
                assert any('restore' in str(call).lower() for call in mock_logger.info.call_args_list)
    
    def test_save_manager_logs_backup_creation(self, mock_logger, tmp_path):
        """Test that SaveManager logs backup creation."""
        with patch('src.save_manager.logger', mock_logger):
            with patch('os.getlogin', return_value='testuser'):
                save_manager = SaveManager()
                
                # Mock file operations
                save_manager.file_ops.file_exists = Mock(return_value=True)
                save_manager.file_ops.ensure_directory_exists = Mock(return_value=Mock(success=True))
                save_manager.file_ops.copy_file = Mock(return_value=Mock(success=True, message="Success"))
                
                # Attempt backup creation
                result = save_manager.create_local_backup()
                
                # Verify backup creation was logged
                assert any('backup' in str(call).lower() for call in mock_logger.info.call_args_list)
    
    @pytest.mark.skipif(not PYTEST_QT_AVAILABLE, reason="pytest-qt not available")
    def test_main_window_logs_initialization(self, mock_logger, qtbot):
        """Test that MainWindow logs initialization."""
        with patch('src.main_window.logger', mock_logger):
            with patch('os.getlogin', return_value='testuser'):
                save_manager = SaveManager()
                window = MainWindow(save_manager)
                qtbot.addWidget(window)
                
                # Verify initialization was logged
                mock_logger.info.assert_called()
    
    @pytest.mark.skipif(not PYTEST_QT_AVAILABLE, reason="pytest-qt not available")
    def test_main_window_logs_restore_action(self, mock_logger, qtbot):
        """Test that MainWindow logs restore actions."""
        with patch('src.main_window.logger', mock_logger):
            with patch('os.getlogin', return_value='testuser'):
                save_manager = SaveManager()
                save_manager.restore_backup = Mock(return_value=Mock(success=True, message="Success"))
                save_manager.list_backups = Mock(return_value=[])
                
                window = MainWindow(save_manager)
                qtbot.addWidget(window)
                
                # Mock a selected backup
                window.get_selected_backup = Mock(return_value="test_backup.savbackup")
                
                # Trigger restore
                window.on_restore_clicked()
                
                # Verify restore was logged
                assert any('restore' in str(call).lower() for call in mock_logger.info.call_args_list)
    
    @pytest.mark.skipif(not PYTEST_QT_AVAILABLE, reason="pytest-qt not available")
    def test_main_window_logs_backup_creation_action(self, mock_logger, qtbot):
        """Test that MainWindow logs backup creation actions."""
        with patch('src.main_window.logger', mock_logger):
            with patch('os.getlogin', return_value='testuser'):
                save_manager = SaveManager()
                save_manager.create_local_backup = Mock(return_value=Mock(success=True, message="Success"))
                save_manager.list_backups = Mock(return_value=[])
                
                window = MainWindow(save_manager)
                qtbot.addWidget(window)
                
                # Trigger backup creation
                window.on_create_backup_clicked()
                
                # Verify backup creation was logged
                assert any('backup' in str(call).lower() for call in mock_logger.info.call_args_list)
    
    def test_logging_config_creates_log_file(self, tmp_path):
        """Test that logging configuration creates log file."""
        log_dir = tmp_path / "logs"
        logger = setup_logging(log_dir)
        
        # Log a test message
        logger.info("Test message")
        
        # Verify log file was created
        log_files = list(log_dir.glob("scumgenics_*.log"))
        assert len(log_files) == 1
        
        # Verify log file contains the message
        log_content = log_files[0].read_text()
        assert "Test message" in log_content
    
    def test_logging_includes_timestamp(self, tmp_path):
        """Test that log entries include timestamps."""
        log_dir = tmp_path / "logs"
        logger = setup_logging(log_dir)
        
        # Log a test message
        logger.info("Timestamp test")
        
        # Read log file
        log_files = list(log_dir.glob("scumgenics_*.log"))
        log_content = log_files[0].read_text()
        
        # Verify timestamp format (YYYY-MM-DD HH:MM:SS)
        import re
        timestamp_pattern = r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}'
        assert re.search(timestamp_pattern, log_content)
    
    def test_logging_includes_exception_details(self, tmp_path):
        """Test that logging includes exception details with exc_info."""
        log_dir = tmp_path / "logs"
        logger = setup_logging(log_dir)
        
        # Log an exception
        try:
            raise ValueError("Test exception")
        except ValueError:
            logger.error("Exception occurred", exc_info=True)
        
        # Read log file
        log_files = list(log_dir.glob("scumgenics_*.log"))
        log_content = log_files[0].read_text()
        
        # Verify exception details are in log
        assert "ValueError" in log_content
        assert "Test exception" in log_content
        assert "Traceback" in log_content
