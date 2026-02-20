"""Unit tests for data models."""
import pytest
from datetime import datetime
from pathlib import Path

from src.result import Result
from src.backup_info import BackupInfo
from src.save_manager_config import SaveManagerConfig


class TestResult:
    """Tests for Result dataclass."""
    
    def test_ok_factory_method(self):
        """Test Result.ok() creates successful result."""
        result = Result.ok("Operation successful")
        assert result.success is True
        assert result.message == "Operation successful"
        assert result.error_details is None
    
    def test_error_factory_method(self):
        """Test Result.error() creates error result."""
        result = Result.error("Operation failed", "File not found")
        assert result.success is False
        assert result.message == "Operation failed"
        assert result.error_details == "File not found"
    
    def test_error_factory_method_without_details(self):
        """Test Result.error() without details parameter."""
        result = Result.error("Operation failed")
        assert result.success is False
        assert result.message == "Operation failed"
        assert result.error_details is None


class TestBackupInfo:
    """Tests for BackupInfo dataclass."""
    
    def test_backup_info_creation(self):
        """Test BackupInfo dataclass creation."""
        timestamp = datetime(2024, 1, 15, 14, 30)
        backup = BackupInfo(
            filename="steamcampaign01_2024-01-15_14-30.savbackup",
            full_path=Path("C:/Users/test/backups/steamcampaign01_2024-01-15_14-30.savbackup"),
            timestamp=timestamp,
            size_bytes=2048
        )
        assert backup.filename == "steamcampaign01_2024-01-15_14-30.savbackup"
        assert backup.timestamp == timestamp
        assert backup.size_bytes == 2048
    
    def test_display_name(self):
        """Test BackupInfo.display_name() formatting."""
        timestamp = datetime(2024, 1, 15, 14, 30)
        backup = BackupInfo(
            filename="steamcampaign01_2024-01-15_14-30.savbackup",
            full_path=Path("C:/Users/test/backups/steamcampaign01_2024-01-15_14-30.savbackup"),
            timestamp=timestamp,
            size_bytes=2048
        )
        display = backup.display_name()
        assert display == "2024-01-15 14:30 (2 KB)"
    
    def test_display_name_large_file(self):
        """Test BackupInfo.display_name() with larger file size."""
        timestamp = datetime(2024, 1, 15, 14, 30)
        backup = BackupInfo(
            filename="steamcampaign01_2024-01-15_14-30.savbackup",
            full_path=Path("C:/Users/test/backups/steamcampaign01_2024-01-15_14-30.savbackup"),
            timestamp=timestamp,
            size_bytes=1024000  # ~1000 KB
        )
        display = backup.display_name()
        assert display == "2024-01-15 14:30 (1000 KB)"


class TestSaveManagerConfig:
    """Tests for SaveManagerConfig dataclass."""
    
    def test_save_manager_config_creation(self):
        """Test SaveManagerConfig dataclass creation."""
        config = SaveManagerConfig(
            username="testuser",
            main_save_path=Path("C:/Users/testuser/AppData/Roaming/Glaiel Games/Mewgenics/76561197960287930/saves/steamcampaign01.sav"),
            backup_directory=Path("C:/Users/testuser/AppData/Roaming/Glaiel Games/Mewgenics/76561197960287930/saves/backups"),
            local_backup_directory=Path("./backups")
        )
        assert config.username == "testuser"
        assert config.main_save_path.name == "steamcampaign01.sav"
        assert config.backup_directory.name == "backups"
        assert config.local_backup_directory == Path("./backups")
