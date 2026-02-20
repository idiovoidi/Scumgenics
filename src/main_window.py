"""MainWindow class for the Scumgenics save manager GUI."""
import logging
import os
import subprocess
from typing import List, Optional
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QListWidget, 
    QPushButton, QLabel, QMessageBox, QTabWidget, QDialog
)

from src.save_manager import SaveManager
from src.backup_info import BackupInfo
from src.options_dialog import OptionsDialog

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
        
        # Create central widget and tab widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Create tab widget
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)
        
        # Create Backups tab
        backups_tab = QWidget()
        backups_layout = QVBoxLayout(backups_tab)
        
        # Create QListWidget for backup list display
        self.backup_list = QListWidget()
        backups_layout.addWidget(self.backup_list)
        
        # Create QPushButton for "Restore" (initially disabled)
        self.restore_button = QPushButton("Restore")
        self.restore_button.setEnabled(False)
        backups_layout.addWidget(self.restore_button)
        
        # Create QPushButton for "Create Local Backup"
        self.create_backup_button = QPushButton("Create External Backup")
        backups_layout.addWidget(self.create_backup_button)
        
        # Create QPushButton for "Launch Game"
        self.launch_game_button = QPushButton("Launch Game")
        self.launch_game_button.clicked.connect(self.on_launch_game_clicked)
        backups_layout.addWidget(self.launch_game_button)
        
        # Create QLabel for status messages
        self.status_label = QLabel("")
        backups_layout.addWidget(self.status_label)
        
        self.tabs.addTab(backups_tab, "Backups")
        
        # Create Options tab
        options_tab = QWidget()
        options_layout = QVBoxLayout(options_tab)
        
        # Current path display
        self.current_path_label = QLabel()
        self._update_path_label()
        options_layout.addWidget(self.current_path_label)
        
        # Game executable display
        self.game_exe_label = QLabel()
        self._update_game_exe_label()
        options_layout.addWidget(self.game_exe_label)
        
        # Options button
        self.options_button = QPushButton("Change Settings...")
        self.options_button.clicked.connect(self.on_options_clicked)
        options_layout.addWidget(self.options_button)
        
        # Local backup folder section
        local_backup_label = QLabel(f"\nLocal Backup Folder:\n{self.save_manager.get_local_backup_directory().absolute()}")
        options_layout.addWidget(local_backup_label)
        
        # Open backup folder button
        self.open_backup_folder_button = QPushButton("Open Backup Folder")
        self.open_backup_folder_button.clicked.connect(self.on_open_backup_folder_clicked)
        options_layout.addWidget(self.open_backup_folder_button)
        
        # Add stretch to push everything to the top
        options_layout.addStretch()
        
        self.tabs.addTab(options_tab, "Options")
        
        # Connect signals (will be implemented in subtask 8.6)
        self.backup_list.itemSelectionChanged.connect(self._on_selection_changed)
        self.restore_button.clicked.connect(self.on_restore_clicked)
        self.create_backup_button.clicked.connect(self.on_create_backup_clicked)
        
        # Update launch button state based on executable configuration
        self._update_launch_button_state()
        
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
    
    def _update_path_label(self):
        """Update the current path label."""
        if self.save_manager.config.custom_save_folder:
            path_text = f"Current Save Folder: {self.save_manager.config.custom_save_folder}"
        else:
            path_text = f"Current Save Folder: Auto-detected\n{self.save_manager.get_main_save_path().parent}"
        self.current_path_label.setText(path_text)
    
    def _update_game_exe_label(self):
        """Update the game executable label."""
        if self.save_manager.config.game_executable_path:
            exe_text = f"\nGame Executable: {self.save_manager.config.game_executable_path}"
        else:
            exe_text = "\nGame Executable: Not configured"
        self.game_exe_label.setText(exe_text)
    
    def _update_launch_button_state(self):
        """Update the launch game button enabled state."""
        has_exe = self.save_manager.config.game_executable_path is not None
        self.launch_game_button.setEnabled(has_exe)
        if not has_exe:
            self.launch_game_button.setToolTip("Configure game executable in Options tab")
    
    def on_options_clicked(self):
        """Handle options button click."""
        dialog = OptionsDialog(
            self, 
            self.save_manager.config.custom_save_folder,
            self.save_manager.config.game_executable_path
        )
        if dialog.exec() == QDialog.DialogCode.Accepted:
            custom_path = dialog.get_custom_path()
            self.save_manager.set_custom_save_folder(custom_path)
            self._update_path_label()
            
            # Update game executable path
            game_exe_path = dialog.get_game_exe_path()
            self.save_manager.set_game_executable_path(game_exe_path)
            self._update_game_exe_label()
            self._update_launch_button_state()
            
            # Refresh backup list with new path
            self._refresh_backup_list()
            
            # Show confirmation
            messages = []
            if custom_path:
                messages.append(f"Save folder updated to:\n{custom_path}")
            else:
                messages.append("Save folder reset to auto-detect")
            
            if game_exe_path:
                messages.append(f"Game executable set to:\n{game_exe_path}")
            elif dialog.exe_input.text().strip() == "" and self.save_manager.config.game_executable_path is None:
                pass  # No change
            else:
                messages.append("Game executable cleared")
            
            self.display_success("\n\n".join(messages))
    
    def on_open_backup_folder_clicked(self):
        """Handle open backup folder button click."""
        backup_folder = self.save_manager.get_local_backup_directory().absolute()
        
        # Ensure the folder exists
        if not backup_folder.exists():
            self.display_error(f"Backup folder does not exist:\n{backup_folder}")
            return
        
        try:
            # Open folder in Windows Explorer
            os.startfile(backup_folder)
            logger.info(f"Opened backup folder: {backup_folder}")
        except Exception as e:
            logger.error(f"Failed to open backup folder: {e}")
            self.display_error(f"Failed to open backup folder:\n{str(e)}")
    
    def on_launch_game_clicked(self):
        """Handle launch game button click."""
        logger.info("User initiated game launch")
        result = self.save_manager.launch_game()
        
        if not result.success:
            logger.error(f"Game launch failed: {result.message}")
            error_message = result.message
            if result.error_details:
                error_message += f"\n\n{result.error_details}"
            self.display_error(error_message)
