"""Options dialog for application settings."""
import logging
from pathlib import Path
from typing import Optional
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QLineEdit, QFileDialog, QMessageBox
)

logger = logging.getLogger("scumgenics.options_dialog")


class OptionsDialog(QDialog):
    """Dialog for configuring application options."""
    
    def __init__(self, parent=None, current_path: Optional[Path] = None, game_exe_path: Optional[Path] = None):
        """Initialize options dialog.
        
        Args:
            parent: Parent widget
            current_path: Current custom save folder path
            game_exe_path: Current game executable path
        """
        super().__init__(parent)
        self.setWindowTitle("Options")
        self.setMinimumWidth(500)
        
        self.custom_path = current_path
        self.game_exe_path = game_exe_path
        
        # Create layout
        layout = QVBoxLayout(self)
        
        # Custom save folder section
        folder_label = QLabel("Custom Save Folder (leave empty for auto-detect):")
        layout.addWidget(folder_label)
        
        # Path input with browse button
        path_layout = QHBoxLayout()
        self.path_input = QLineEdit()
        if current_path:
            self.path_input.setText(str(current_path))
        self.path_input.setPlaceholderText("Auto-detect from Windows username")
        path_layout.addWidget(self.path_input)
        
        self.browse_button = QPushButton("Browse...")
        self.browse_button.clicked.connect(self._on_browse_clicked)
        path_layout.addWidget(self.browse_button)
        
        layout.addLayout(path_layout)
        
        # Clear button
        self.clear_button = QPushButton("Clear (Use Auto-Detect)")
        self.clear_button.clicked.connect(self._on_clear_clicked)
        layout.addWidget(self.clear_button)
        
        # Spacer
        layout.addWidget(QLabel(""))
        
        # Game executable section
        exe_label = QLabel("Game Executable Path:")
        layout.addWidget(exe_label)
        
        # Exe path input with browse button
        exe_layout = QHBoxLayout()
        self.exe_input = QLineEdit()
        if game_exe_path:
            self.exe_input.setText(str(game_exe_path))
        self.exe_input.setPlaceholderText("Path to Mewgenics.exe")
        exe_layout.addWidget(self.exe_input)
        
        self.browse_exe_button = QPushButton("Browse...")
        self.browse_exe_button.clicked.connect(self._on_browse_exe_clicked)
        exe_layout.addWidget(self.browse_exe_button)
        
        layout.addLayout(exe_layout)
        
        # Clear exe button
        self.clear_exe_button = QPushButton("Clear")
        self.clear_exe_button.clicked.connect(self._on_clear_exe_clicked)
        layout.addWidget(self.clear_exe_button)
        
        # Dialog buttons
        button_layout = QHBoxLayout()
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self._on_ok_clicked)
        button_layout.addWidget(self.ok_button)
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)
        
        layout.addLayout(button_layout)
    
    def _on_browse_clicked(self):
        """Handle browse button click."""
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Save Folder",
            str(self.custom_path) if self.custom_path else ""
        )
        if folder:
            self.path_input.setText(folder)
    
    def _on_clear_clicked(self):
        """Handle clear button click."""
        self.path_input.clear()
    
    def _on_browse_exe_clicked(self):
        """Handle browse exe button click."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Game Executable",
            str(self.game_exe_path.parent) if self.game_exe_path else "",
            "Executable Files (*.exe);;All Files (*.*)"
        )
        if file_path:
            self.exe_input.setText(file_path)
    
    def _on_clear_exe_clicked(self):
        """Handle clear exe button click."""
        self.exe_input.clear()
    
    def _on_ok_clicked(self):
        """Handle OK button click."""
        path_text = self.path_input.text().strip()
        
        if path_text:
            path = Path(path_text)
            # Validate that the path exists
            if not path.exists():
                QMessageBox.warning(
                    self,
                    "Invalid Path",
                    f"The specified folder does not exist:\n{path}"
                )
                return
            
            # Check if save file exists in the custom path
            save_file = path / "steamcampaign01.sav"
            if not save_file.exists():
                response = QMessageBox.question(
                    self,
                    "Save File Not Found",
                    f"The save file was not found at:\n{save_file}\n\nDo you want to use this path anyway?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )
                if response == QMessageBox.StandardButton.No:
                    return
            
            self.custom_path = path
        else:
            self.custom_path = None
        
        # Handle game executable path
        exe_text = self.exe_input.text().strip()
        if exe_text:
            exe_path = Path(exe_text)
            if not exe_path.exists():
                QMessageBox.warning(
                    self,
                    "Invalid Path",
                    f"The specified executable does not exist:\n{exe_path}"
                )
                return
            self.game_exe_path = exe_path
        else:
            self.game_exe_path = None
        
        self.accept()
    
    def get_custom_path(self) -> Optional[Path]:
        """Get the selected custom path.
        
        Returns:
            Selected custom path or None
        """
        return self.custom_path
    
    def get_game_exe_path(self) -> Optional[Path]:
        """Get the selected game executable path.
        
        Returns:
            Selected game executable path or None
        """
        return self.game_exe_path
