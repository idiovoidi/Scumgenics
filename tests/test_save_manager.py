"""Unit tests for SaveManager class."""
import pytest
import os
from pathlib import Path
from datetime import datetime
from unittest.mock import patch, MagicMock
from src.save_manager import SaveManager
from src.backup_info import BackupInfo
from src.result import Result


class TestSaveManagerInitialization:
    """Test suite for SaveManager initialization."""
    
    @patch('os.getlogin')
    def test_init_detects_username_with_getlogin(self, mock_getlogin):
        """Test that __init__ detects username using os.getlogin()."""
        mock_getlogin.return_value = "testuser"
        
        manager = SaveManager()
        
        assert manager.config.username == "testuser"
        mock_getlogin.assert_called_once()
    
    @patch('os.getlogin', side_effect=OSError)
    @patch.dict(os.environ, {'USERNAME': 'envuser'})
    def test_init_falls_back_to_environment_variable(self, mock_getlogin):
        """Test that __init__ falls back to os.environ['USERNAME'] when getlogin fails."""
        manager = SaveManager()
        
        assert manager.config.username == "envuser"
    
    @patch('os.getlogin', side_effect=OSError)
    @patch.dict(os.environ, {}, clear=True)
    def test_init_raises_error_when_username_not_detected(self, mock_getlogin):
        """Test that __init__ raises RuntimeError when username cannot be detected."""
        with pytest.raises(RuntimeError, match="Unable to detect Windows username"):
            SaveManager()
    
    @patch('os.getlogin')
    def test_init_constructs_paths_correctly(self, mock_getlogin):
        """Test that __init__ constructs paths using PathBuilder."""
        mock_getlogin.return_value = "testuser"
        
        manager = SaveManager()
        
        assert "testuser" in str(manager.config.main_save_path)
        assert manager.config.main_save_path.name == "steamcampaign01.sav"
        assert manager.config.backup_directory.name == "backups"
        assert manager.config.local_backup_directory == Path("./backups")
    
    @patch('os.getlogin')
    def test_init_creates_path_builder_and_file_operations(self, mock_getlogin):
        """Test that __init__ creates PathBuilder and FileOperations instances."""
        mock_getlogin.return_value = "testuser"
        
        manager = SaveManager()
        
        assert manager.path_builder is not None
        assert manager.file_ops is not None


class TestSaveManagerPathGetters:
    """Test suite for SaveManager path getter methods."""
    
    @patch('os.getlogin')
    def test_get_main_save_path(self, mock_getlogin):
        """Test get_main_save_path returns correct path."""
        mock_getlogin.return_value = "testuser"
        manager = SaveManager()
        
        path = manager.get_main_save_path()
        
        assert isinstance(path, Path)
        assert path.name == "steamcampaign01.sav"
        assert "testuser" in str(path)
    
    @patch('os.getlogin')
    def test_get_backup_directory(self, mock_getlogin):
        """Test get_backup_directory returns correct path."""
        mock_getlogin.return_value = "testuser"
        manager = SaveManager()
        
        path = manager.get_backup_directory()
        
        assert isinstance(path, Path)
        assert path.name == "backups"
    
    @patch('os.getlogin')
    def test_get_local_backup_directory(self, mock_getlogin):
        """Test get_local_backup_directory returns correct path."""
        mock_getlogin.return_value = "testuser"
        manager = SaveManager()
        
        path = manager.get_local_backup_directory()
        
        assert isinstance(path, Path)
        assert path == Path("./backups")


class TestSaveManagerVerifyMainSave:
    """Test suite for verify_main_save_exists method."""
    
    @patch('os.getlogin')
    def test_verify_main_save_exists_returns_true_when_file_exists(self, mock_getlogin, tmp_path):
        """Test verify_main_save_exists returns True when main save exists."""
        mock_getlogin.return_value = "testuser"
        manager = SaveManager()
        
        # Create a temporary main save file
        main_save = tmp_path / "steamcampaign01.sav"
        main_save.write_text("save data")
        manager.config.main_save_path = main_save
        
        assert manager.verify_main_save_exists() is True
    
    @patch('os.getlogin')
    def test_verify_main_save_exists_returns_false_when_file_missing(self, mock_getlogin, tmp_path):
        """Test verify_main_save_exists returns False when main save doesn't exist."""
        mock_getlogin.return_value = "testuser"
        manager = SaveManager()
        
        # Set path to nonexistent file
        manager.config.main_save_path = tmp_path / "nonexistent.sav"
        
        assert manager.verify_main_save_exists() is False


class TestSaveManagerListBackups:
    """Test suite for list_backups method."""
    
    @patch('os.getlogin')
    def test_list_backups_returns_empty_list_when_no_backups(self, mock_getlogin, tmp_path):
        """Test list_backups returns empty list when no backups exist."""
        mock_getlogin.return_value = "testuser"
        manager = SaveManager()
        
        # Set directories to empty temp directories
        manager.config.backup_directory = tmp_path / "backups"
        manager.config.local_backup_directory = tmp_path / "local_backups"
        manager.config.backup_directory.mkdir()
        manager.config.local_backup_directory.mkdir()
        
        backups = manager.list_backups()
        
        assert len(backups) == 0
    
    @patch('os.getlogin')
    def test_list_backups_finds_backups_in_backup_directory(self, mock_getlogin, tmp_path):
        """Test list_backups finds backups in backup directory."""
        mock_getlogin.return_value = "testuser"
        manager = SaveManager()
        
        # Create backup directory with backup files
        backup_dir = tmp_path / "backups"
        backup_dir.mkdir()
        backup1 = backup_dir / "steamcampaign01_2024-01-15_14-30.savbackup"
        backup1.write_text("backup data")
        
        manager.config.backup_directory = backup_dir
        manager.config.local_backup_directory = tmp_path / "local_backups"
        manager.config.local_backup_directory.mkdir()
        
        backups = manager.list_backups()
        
        assert len(backups) == 1
        assert backups[0].filename == "steamcampaign01_2024-01-15_14-30.savbackup"
    
    @patch('os.getlogin')
    def test_list_backups_finds_backups_in_local_directory(self, mock_getlogin, tmp_path):
        """Test list_backups finds backups in local backup directory."""
        mock_getlogin.return_value = "testuser"
        manager = SaveManager()
        
        # Create local backup directory with backup files
        local_dir = tmp_path / "local_backups"
        local_dir.mkdir()
        backup1 = local_dir / "steamcampaign01_2024-01-15_14-30.savbackup"
        backup1.write_text("backup data")
        
        manager.config.backup_directory = tmp_path / "backups"
        manager.config.backup_directory.mkdir()
        manager.config.local_backup_directory = local_dir
        
        backups = manager.list_backups()
        
        assert len(backups) == 1
        assert backups[0].filename == "steamcampaign01_2024-01-15_14-30.savbackup"
    
    @patch('os.getlogin')
    def test_list_backups_combines_both_directories(self, mock_getlogin, tmp_path):
        """Test list_backups combines backups from both directories."""
        mock_getlogin.return_value = "testuser"
        manager = SaveManager()
        
        # Create backup directory
        backup_dir = tmp_path / "backups"
        backup_dir.mkdir()
        backup1 = backup_dir / "steamcampaign01_2024-01-15_14-30.savbackup"
        backup1.write_text("backup data 1")
        
        # Create local backup directory
        local_dir = tmp_path / "local_backups"
        local_dir.mkdir()
        backup2 = local_dir / "steamcampaign01_2024-01-16_10-00.savbackup"
        backup2.write_text("backup data 2")
        
        manager.config.backup_directory = backup_dir
        manager.config.local_backup_directory = local_dir
        
        backups = manager.list_backups()
        
        assert len(backups) == 2
    
    @patch('os.getlogin')
    def test_list_backups_sorts_by_timestamp_descending(self, mock_getlogin, tmp_path):
        """Test list_backups sorts backups by timestamp in descending order."""
        mock_getlogin.return_value = "testuser"
        manager = SaveManager()
        
        # Create backup directory with multiple backups
        backup_dir = tmp_path / "backups"
        backup_dir.mkdir()
        
        backup1 = backup_dir / "steamcampaign01_2024-01-15_14-30.savbackup"
        backup1.write_text("backup 1")
        
        backup2 = backup_dir / "steamcampaign01_2024-01-16_10-00.savbackup"
        backup2.write_text("backup 2")
        
        backup3 = backup_dir / "steamcampaign01_2024-01-14_08-15.savbackup"
        backup3.write_text("backup 3")
        
        manager.config.backup_directory = backup_dir
        manager.config.local_backup_directory = tmp_path / "local_backups"
        manager.config.local_backup_directory.mkdir()
        
        backups = manager.list_backups()
        
        assert len(backups) == 3
        # Should be sorted newest first
        assert backups[0].filename == "steamcampaign01_2024-01-16_10-00.savbackup"
        assert backups[1].filename == "steamcampaign01_2024-01-15_14-30.savbackup"
        assert backups[2].filename == "steamcampaign01_2024-01-14_08-15.savbackup"
    
    @patch('os.getlogin')
    def test_list_backups_creates_backup_info_objects(self, mock_getlogin, tmp_path):
        """Test list_backups creates BackupInfo objects with correct data."""
        mock_getlogin.return_value = "testuser"
        manager = SaveManager()
        
        # Create backup directory with backup file
        backup_dir = tmp_path / "backups"
        backup_dir.mkdir()
        backup1 = backup_dir / "steamcampaign01_2024-01-15_14-30.savbackup"
        backup1.write_text("backup data")
        
        manager.config.backup_directory = backup_dir
        manager.config.local_backup_directory = tmp_path / "local_backups"
        manager.config.local_backup_directory.mkdir()
        
        backups = manager.list_backups()
        
        assert len(backups) == 1
        backup_info = backups[0]
        assert isinstance(backup_info, BackupInfo)
        assert backup_info.filename == "steamcampaign01_2024-01-15_14-30.savbackup"
        assert backup_info.full_path == backup1
        assert backup_info.timestamp == datetime(2024, 1, 15, 14, 30)
        assert backup_info.size_bytes > 0


class TestSaveManagerRestoreBackup:
    """Test suite for restore_backup method."""
    
    @patch('os.getlogin')
    def test_restore_backup_fails_when_main_save_missing(self, mock_getlogin, tmp_path):
        """Test restore_backup fails when main save doesn't exist."""
        mock_getlogin.return_value = "testuser"
        manager = SaveManager()
        
        manager.config.main_save_path = tmp_path / "steamcampaign01.sav"
        
        result = manager.restore_backup("steamcampaign01_2024-01-15_14-30.savbackup")
        
        assert result.success is False
        assert "main save file not found" in result.message.lower()
    
    @patch('os.getlogin')
    def test_restore_backup_fails_when_backup_not_found(self, mock_getlogin, tmp_path):
        """Test restore_backup fails when backup file doesn't exist."""
        mock_getlogin.return_value = "testuser"
        manager = SaveManager()
        
        # Create main save
        main_save = tmp_path / "saves" / "steamcampaign01.sav"
        main_save.parent.mkdir(parents=True)
        main_save.write_text("main save data")
        
        manager.config.main_save_path = main_save
        manager.config.backup_directory = tmp_path / "backups"
        manager.config.backup_directory.mkdir()
        manager.config.local_backup_directory = tmp_path / "local_backups"
        manager.config.local_backup_directory.mkdir()
        
        result = manager.restore_backup("nonexistent_backup.savbackup")
        
        assert result.success is False
        assert "backup file not found" in result.message.lower()
    
    @patch('os.getlogin')
    def test_restore_backup_success_from_backup_directory(self, mock_getlogin, tmp_path):
        """Test successful restore from backup directory."""
        mock_getlogin.return_value = "testuser"
        manager = SaveManager()
        
        # Create main save
        saves_dir = tmp_path / "saves"
        saves_dir.mkdir()
        main_save = saves_dir / "steamcampaign01.sav"
        main_save.write_text("old save data")
        
        # Create backup
        backup_dir = tmp_path / "backups"
        backup_dir.mkdir()
        backup_file = backup_dir / "steamcampaign01_2024-01-15_14-30.savbackup"
        backup_file.write_text("backup save data")
        
        manager.config.main_save_path = main_save
        manager.config.backup_directory = backup_dir
        manager.config.local_backup_directory = tmp_path / "local_backups"
        manager.config.local_backup_directory.mkdir()
        
        result = manager.restore_backup("steamcampaign01_2024-01-15_14-30.savbackup")
        
        assert result.success is True
        assert "restored successfully" in result.message.lower()
        assert main_save.exists()
        assert main_save.read_text() == "backup save data"
    
    @patch('os.getlogin')
    def test_restore_backup_success_from_local_directory(self, mock_getlogin, tmp_path):
        """Test successful restore from local backup directory."""
        mock_getlogin.return_value = "testuser"
        manager = SaveManager()
        
        # Create main save
        saves_dir = tmp_path / "saves"
        saves_dir.mkdir()
        main_save = saves_dir / "steamcampaign01.sav"
        main_save.write_text("old save data")
        
        # Create local backup
        local_dir = tmp_path / "local_backups"
        local_dir.mkdir()
        backup_file = local_dir / "steamcampaign01_2024-01-15_14-30.savbackup"
        backup_file.write_text("local backup save data")
        
        manager.config.main_save_path = main_save
        manager.config.backup_directory = tmp_path / "backups"
        manager.config.backup_directory.mkdir()
        manager.config.local_backup_directory = local_dir
        
        result = manager.restore_backup("steamcampaign01_2024-01-15_14-30.savbackup")
        
        assert result.success is True
        assert "restored successfully" in result.message.lower()
        assert main_save.exists()
        assert main_save.read_text() == "local backup save data"
    
    @patch('os.getlogin')
    def test_restore_backup_deletes_main_save_before_copy(self, mock_getlogin, tmp_path):
        """Test that restore_backup deletes main save before copying."""
        mock_getlogin.return_value = "testuser"
        manager = SaveManager()
        
        # Create main save
        saves_dir = tmp_path / "saves"
        saves_dir.mkdir()
        main_save = saves_dir / "steamcampaign01.sav"
        main_save.write_text("old save data")
        
        # Create backup
        backup_dir = tmp_path / "backups"
        backup_dir.mkdir()
        backup_file = backup_dir / "steamcampaign01_2024-01-15_14-30.savbackup"
        backup_file.write_text("new save data")
        
        manager.config.main_save_path = main_save
        manager.config.backup_directory = backup_dir
        manager.config.local_backup_directory = tmp_path / "local_backups"
        manager.config.local_backup_directory.mkdir()
        
        result = manager.restore_backup("steamcampaign01_2024-01-15_14-30.savbackup")
        
        assert result.success is True
        # Verify content was replaced
        assert main_save.read_text() == "new save data"


class TestSaveManagerCreateLocalBackup:
    """Test suite for create_local_backup method."""
    
    @patch('os.getlogin')
    def test_create_local_backup_fails_when_main_save_missing(self, mock_getlogin, tmp_path):
        """Test create_local_backup fails when main save doesn't exist."""
        mock_getlogin.return_value = "testuser"
        manager = SaveManager()
        
        manager.config.main_save_path = tmp_path / "steamcampaign01.sav"
        
        result = manager.create_local_backup()
        
        assert result.success is False
        assert "main save file not found" in result.message.lower()
    
    @patch('os.getlogin')
    def test_create_local_backup_creates_directory_if_missing(self, mock_getlogin, tmp_path):
        """Test create_local_backup creates local backup directory if it doesn't exist."""
        mock_getlogin.return_value = "testuser"
        manager = SaveManager()
        
        # Create main save
        main_save = tmp_path / "steamcampaign01.sav"
        main_save.write_text("save data")
        
        local_dir = tmp_path / "local_backups"
        
        manager.config.main_save_path = main_save
        manager.config.local_backup_directory = local_dir
        
        result = manager.create_local_backup()
        
        assert result.success is True
        assert local_dir.exists()
        assert local_dir.is_dir()
    
    @patch('os.getlogin')
    def test_create_local_backup_success(self, mock_getlogin, tmp_path):
        """Test successful local backup creation."""
        mock_getlogin.return_value = "testuser"
        manager = SaveManager()
        
        # Create main save
        main_save = tmp_path / "steamcampaign01.sav"
        main_save.write_text("save data to backup")
        
        local_dir = tmp_path / "local_backups"
        local_dir.mkdir()
        
        manager.config.main_save_path = main_save
        manager.config.local_backup_directory = local_dir
        
        result = manager.create_local_backup()
        
        assert result.success is True
        assert "created successfully" in result.message.lower()
        
        # Verify backup file was created
        backup_files = list(local_dir.glob("steamcampaign01_*.savbackup"))
        assert len(backup_files) == 1
        assert backup_files[0].read_text() == "save data to backup"
    
    @patch('os.getlogin')
    def test_create_local_backup_uses_timestamped_filename(self, mock_getlogin, tmp_path):
        """Test create_local_backup uses timestamped filename format."""
        mock_getlogin.return_value = "testuser"
        manager = SaveManager()
        
        # Create main save
        main_save = tmp_path / "steamcampaign01.sav"
        main_save.write_text("save data")
        
        local_dir = tmp_path / "local_backups"
        local_dir.mkdir()
        
        manager.config.main_save_path = main_save
        manager.config.local_backup_directory = local_dir
        
        result = manager.create_local_backup()
        
        assert result.success is True
        
        # Verify filename format
        backup_files = list(local_dir.glob("steamcampaign01_*.savbackup"))
        assert len(backup_files) == 1
        
        # Check filename matches pattern
        import re
        pattern = r"steamcampaign01_\d{4}-\d{2}-\d{2}_\d{2}-\d{2}\.savbackup"
        assert re.match(pattern, backup_files[0].name)
