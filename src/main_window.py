"""MainWindow class for the Scumgenics save manager GUI."""
import logging
from typing import List, Optional
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QListWidget, 
    QPushButton, QLabel, QMessageBox
)

from src.save_manager import SaveManager
from src.backup_info import BackupInfo

logger = logging.getLogger("scumgenics.main_window")


class MainWindow(QMainWindow):
    """Main window for the Scumgenics save manager application."""
    
    def __init__(self, save_manager: SaveManager):
        """Initialize the main window with title 'Scumgenics'.
        
        Args:
            save_manager: SaveManager instance for file operations
        """
        super().__init__()
        
        logger.info("Initializing MainWindow")
        self.save_manager = save_manager
        
        # Set window title
        self.setWindowTitle("Scumgenics")
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Create QListWidget for backup list display
        self.backup_list = QListWidget()
        layout.addWidget(self.backup_list)
        
        # Create QPushButton for "Restore" (initially disabled)
        self.restore_button = QPushButton("Restore")
        self.restore_button.setEnabled(False)
        layout.addWidget(self.restore_button)
        
        # Create QPushButton for "Create Local Backup"
        self.create_backup_button = QPushButton("Create Local Backup")
        layout.addWidget(self.create_backup_button)
        
        # Create QLabel for status messages
        self.status_label = QLabel("")
        layout.addWidget(self.status_label)
        
        # Connect signals (will be implemented in subtask 8.6)
        self.backup_list.itemSelectionChanged.connect(self._on_selection_changed)
        self.restore_button.clicked.connect(self.on_restore_clicked)
        self.create_backup_button.clicked.connect(self.on_create_backup_clicked)
        
        logger.debug("MainWindow initialization complete")
    
    def _on_selection_changed(self):
        """Handle backup list selection changes to update restore button state."""
        # Enable restore button only when a backup is selected
        has_selection = len(self.backup_list.selectedItems()) > 0
        self.restore_button.setEnabled(has_selection)
    
    def display_backups(self, backups: List[BackupInfo]) -> None:
        """Display the list of available backups in the UI.
        
        Args:
            backups: List of BackupInfo objects to display
        """
        self.backup_list.clear()
        for backup in backups:
            self.backup_list.addItem(backup.display_name())
    
    def display_error(self, message: str) -> None:
        """Show error message dialog to user.
        
        Args:
            message: Error message to display
        """
        QMessageBox.critical(self, "Error", message)
    
    def display_success(self, message: str) -> None:
        """Show success message dialog to user.
        
        Args:
            message: Success message to display
        """
        QMessageBox.information(self, "Success", message)
    
    def get_selected_backup(self) -> Optional[str]:
        """Return the currently selected backup filename.
        
        Returns:
            Selected backup filename or None if no selection
        """
        selected_items = self.backup_list.selectedItems()
        if not selected_items:
            return None
        
        # Get the selected display name
        display_name = selected_items[0].text()
        
        # Find the corresponding backup filename
        backups = self.save_manager.list_backups()
        for backup in backups:
            if backup.display_name() == display_name:
                return backup.filename
        
        return None
    
    def on_restore_clicked(self) -> None:
        """Handle restore button click event."""
        backup_filename = self.get_selected_backup()
        if backup_filename is None:
            logger.warning("Restore clicked but no backup selected")
            self.display_error("No backup selected")
            return
        
        logger.info(f"User initiated restore for backup: {backup_filename}")
        
        # Call SaveManager.restore_backup()
        result = self.save_manager.restore_backup(backup_filename)
        
        # Display success/error messages based on Result
        if result.success:
            logger.info(f"Restore successful: {backup_filename}")
            self.display_success(result.message)
            # Refresh backup list after successful operation
            self._refresh_backup_list()
        else:
            logger.error(f"Restore failed: {result.message}")
            error_message = result.message
            if result.error_details:
                error_message += f"\n\n{result.error_details}"
            self.display_error(error_message)
    
    def on_create_backup_clicked(self) -> None:
        """Handle create backup button click event."""
        logger.info("User initiated local backup creation")
        
        # Call SaveManager.create_local_backup()
        result = self.save_manager.create_local_backup()
        
        # Display success/error messages based on Result
        if result.success:
            logger.info("Local backup creation successful")
            self.display_success(result.message)
            # Refresh backup list after successful operation
            self._refresh_backup_list()
        else:
            logger.error(f"Local backup creation failed: {result.message}")
            error_message = result.message
            if result.error_details:
                error_message += f"\n\n{result.error_details}"
            self.display_error(error_message)
    
    def _refresh_backup_list(self):
        """Refresh the backup list display."""
        backups = self.save_manager.list_backups()
        self.display_backups(backups)
