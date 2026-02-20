"""Unit tests for FileOperations class."""
import pytest
import tempfile
from pathlib import Path
from src.file_operations import FileOperations
from src.result import Result


class TestFileOperations:
    """Test suite for FileOperations class."""
    
    def test_file_exists_returns_true_for_existing_file(self, tmp_path):
        """Test that file_exists returns True for an existing file."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("test content")
        
        assert FileOperations.file_exists(test_file) is True
    
    def test_file_exists_returns_false_for_nonexistent_file(self, tmp_path):
        """Test that file_exists returns False for a nonexistent file."""
        test_file = tmp_path / "nonexistent.txt"
        
        assert FileOperations.file_exists(test_file) is False
    
    def test_file_exists_returns_false_for_directory(self, tmp_path):
        """Test that file_exists returns False for a directory."""
        test_dir = tmp_path / "test_dir"
        test_dir.mkdir()
        
        assert FileOperations.file_exists(test_dir) is False
    
    def test_delete_file_success(self, tmp_path):
        """Test successful file deletion."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("test content")
        
        result = FileOperations.delete_file(test_file)
        
        assert result.success is True
        assert "deleted successfully" in result.message.lower()
        assert not test_file.exists()
    
    def test_delete_file_not_found(self, tmp_path):
        """Test deletion of nonexistent file."""
        test_file = tmp_path / "nonexistent.txt"
        
        result = FileOperations.delete_file(test_file)
        
        assert result.success is False
        assert "not found" in result.message.lower()
        assert str(test_file) in result.error_details

    def test_copy_file_success(self, tmp_path):
        """Test successful file copy."""
        source = tmp_path / "source.txt"
        destination = tmp_path / "destination.txt"
        source.write_text("test content")
        
        result = FileOperations.copy_file(source, destination)
        
        assert result.success is True
        assert "copied successfully" in result.message.lower()
        assert destination.exists()
        assert destination.read_text() == "test content"
    
    def test_copy_file_source_not_found(self, tmp_path):
        """Test copying nonexistent source file."""
        source = tmp_path / "nonexistent.txt"
        destination = tmp_path / "destination.txt"
        
        result = FileOperations.copy_file(source, destination)
        
        assert result.success is False
        assert "not found" in result.message.lower()
        assert str(source) in result.error_details
    
    def test_rename_file_success(self, tmp_path):
        """Test successful file rename."""
        old_path = tmp_path / "old.txt"
        new_path = tmp_path / "new.txt"
        old_path.write_text("test content")
        
        result = FileOperations.rename_file(old_path, new_path)
        
        assert result.success is True
        assert "renamed successfully" in result.message.lower()
        assert not old_path.exists()
        assert new_path.exists()
        assert new_path.read_text() == "test content"
    
    def test_rename_file_not_found(self, tmp_path):
        """Test renaming nonexistent file."""
        old_path = tmp_path / "nonexistent.txt"
        new_path = tmp_path / "new.txt"
        
        result = FileOperations.rename_file(old_path, new_path)
        
        assert result.success is False
        assert "not found" in result.message.lower()
        assert str(old_path) in result.error_details
    
    def test_list_files_with_pattern(self, tmp_path):
        """Test listing files matching pattern."""
        # Create test files
        (tmp_path / "file1.txt").write_text("content")
        (tmp_path / "file2.txt").write_text("content")
        (tmp_path / "file3.log").write_text("content")
        (tmp_path / "test.txt").write_text("content")
        
        # List files matching pattern
        pattern = r"file\d+\.txt"
        files = FileOperations.list_files(tmp_path, pattern)
        
        assert len(files) == 2
        filenames = [f.name for f in files]
        assert "file1.txt" in filenames
        assert "file2.txt" in filenames
        assert "file3.log" not in filenames
        assert "test.txt" not in filenames
    
    def test_list_files_empty_directory(self, tmp_path):
        """Test listing files in empty directory."""
        empty_dir = tmp_path / "empty"
        empty_dir.mkdir()
        
        files = FileOperations.list_files(empty_dir, r".*")
        
        assert len(files) == 0
    
    def test_list_files_nonexistent_directory(self, tmp_path):
        """Test listing files in nonexistent directory."""
        nonexistent = tmp_path / "nonexistent"
        
        files = FileOperations.list_files(nonexistent, r".*")
        
        assert len(files) == 0
    
    def test_ensure_directory_exists_creates_directory(self, tmp_path):
        """Test directory creation."""
        new_dir = tmp_path / "new_directory"
        
        result = FileOperations.ensure_directory_exists(new_dir)
        
        assert result.success is True
        assert "ready" in result.message.lower()
        assert new_dir.exists()
        assert new_dir.is_dir()
    
    def test_ensure_directory_exists_with_parents(self, tmp_path):
        """Test directory creation with parent directories."""
        nested_dir = tmp_path / "parent" / "child" / "grandchild"
        
        result = FileOperations.ensure_directory_exists(nested_dir)
        
        assert result.success is True
        assert nested_dir.exists()
        assert nested_dir.is_dir()
    
    def test_ensure_directory_exists_already_exists(self, tmp_path):
        """Test ensuring directory exists when it already exists."""
        existing_dir = tmp_path / "existing"
        existing_dir.mkdir()
        
        result = FileOperations.ensure_directory_exists(existing_dir)
        
        assert result.success is True
        assert existing_dir.exists()


class TestResult:
    """Test suite for Result dataclass."""
    
    def test_result_ok_creates_success_result(self):
        """Test Result.ok() creates a successful result."""
        result = Result.ok("Operation successful")
        
        assert result.success is True
        assert result.message == "Operation successful"
        assert result.error_details is None
    
    def test_result_error_creates_error_result(self):
        """Test Result.error() creates an error result."""
        result = Result.error("Operation failed", "Additional details")
        
        assert result.success is False
        assert result.message == "Operation failed"
        assert result.error_details == "Additional details"
    
    def test_result_error_without_details(self):
        """Test Result.error() without details."""
        result = Result.error("Operation failed")
        
        assert result.success is False
        assert result.message == "Operation failed"
        assert result.error_details is None


class TestFileOperationsErrorHandling:
    """Test suite for error handling in FileOperations class."""
    
    def test_delete_file_permission_error(self, tmp_path, mocker):
        """Test delete_file handles PermissionError."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("test content")
        
        # Mock unlink to raise PermissionError
        mocker.patch.object(Path, 'unlink', side_effect=PermissionError("Access denied"))
        
        result = FileOperations.delete_file(test_file)
        
        assert result.success is False
        assert "access denied" in result.message.lower()
        assert "permissions" in result.error_details.lower()
    
    def test_delete_file_os_error(self, tmp_path, mocker):
        """Test delete_file handles OSError."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("test content")
        
        # Mock unlink to raise OSError
        mocker.patch.object(Path, 'unlink', side_effect=OSError("I/O error"))
        
        result = FileOperations.delete_file(test_file)
        
        assert result.success is False
        assert "i/o error" in result.message.lower()
        assert "I/O error" in result.error_details
    
    def test_copy_file_permission_error(self, tmp_path, mocker):
        """Test copy_file handles PermissionError."""
        source = tmp_path / "source.txt"
        destination = tmp_path / "destination.txt"
        source.write_text("test content")
        
        # Mock copy2 to raise PermissionError
        mocker.patch('shutil.copy2', side_effect=PermissionError("Access denied"))
        
        result = FileOperations.copy_file(source, destination)
        
        assert result.success is False
        assert "access denied" in result.message.lower()
        assert "permissions" in result.error_details.lower()
    
    def test_copy_file_os_error(self, tmp_path, mocker):
        """Test copy_file handles OSError."""
        source = tmp_path / "source.txt"
        destination = tmp_path / "destination.txt"
        source.write_text("test content")
        
        # Mock copy2 to raise OSError
        mocker.patch('shutil.copy2', side_effect=OSError("I/O error"))
        
        result = FileOperations.copy_file(source, destination)
        
        assert result.success is False
        assert "i/o error" in result.message.lower()
        assert "I/O error" in result.error_details
    
    def test_rename_file_permission_error(self, tmp_path, mocker):
        """Test rename_file handles PermissionError."""
        old_path = tmp_path / "old.txt"
        new_path = tmp_path / "new.txt"
        old_path.write_text("test content")
        
        # Mock rename to raise PermissionError
        mocker.patch.object(Path, 'rename', side_effect=PermissionError("Access denied"))
        
        result = FileOperations.rename_file(old_path, new_path)
        
        assert result.success is False
        assert "access denied" in result.message.lower()
        assert "permissions" in result.error_details.lower()
    
    def test_rename_file_os_error(self, tmp_path, mocker):
        """Test rename_file handles OSError."""
        old_path = tmp_path / "old.txt"
        new_path = tmp_path / "new.txt"
        old_path.write_text("test content")
        
        # Mock rename to raise OSError
        mocker.patch.object(Path, 'rename', side_effect=OSError("I/O error"))
        
        result = FileOperations.rename_file(old_path, new_path)
        
        assert result.success is False
        assert "i/o error" in result.message.lower()
        assert "I/O error" in result.error_details
    
    def test_list_files_permission_error(self, tmp_path, mocker):
        """Test list_files handles PermissionError."""
        test_dir = tmp_path / "test_dir"
        test_dir.mkdir()
        
        # Mock iterdir to raise PermissionError
        mocker.patch.object(Path, 'iterdir', side_effect=PermissionError("Access denied"))
        
        files = FileOperations.list_files(test_dir, r".*")
        
        # Should return empty list on error
        assert len(files) == 0
    
    def test_list_files_os_error(self, tmp_path, mocker):
        """Test list_files handles OSError."""
        test_dir = tmp_path / "test_dir"
        test_dir.mkdir()
        
        # Mock iterdir to raise OSError
        mocker.patch.object(Path, 'iterdir', side_effect=OSError("I/O error"))
        
        files = FileOperations.list_files(test_dir, r".*")
        
        # Should return empty list on error
        assert len(files) == 0
    
    def test_ensure_directory_exists_permission_error(self, tmp_path, mocker):
        """Test ensure_directory_exists handles PermissionError."""
        new_dir = tmp_path / "new_directory"
        
        # Mock mkdir to raise PermissionError
        mocker.patch.object(Path, 'mkdir', side_effect=PermissionError("Access denied"))
        
        result = FileOperations.ensure_directory_exists(new_dir)
        
        assert result.success is False
        assert "access denied" in result.message.lower()
        assert "permissions" in result.error_details.lower()
    
    def test_ensure_directory_exists_os_error(self, tmp_path, mocker):
        """Test ensure_directory_exists handles OSError."""
        new_dir = tmp_path / "new_directory"
        
        # Mock mkdir to raise OSError
        mocker.patch.object(Path, 'mkdir', side_effect=OSError("I/O error"))
        
        result = FileOperations.ensure_directory_exists(new_dir)
        
        assert result.success is False
        assert "i/o error" in result.message.lower()
        assert "I/O error" in result.error_details
