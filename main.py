"""Main entry point for the Scumgenics save manager application."""
import sys
import logging
from PyQt6.QtWidgets import QApplication, QMessageBox

from src.save_manager import SaveManager
from src.main_window import MainWindow
from src.logging_config import setup_logging


def main():
    """Initialize and run the Scumgenics application."""
    # Set up logging
    logger = setup_logging()
    logger.info("Starting Scumgenics Save Manager")
    
    # Create QApplication instance
    app = QApplication(sys.argv)
    
    try:
        # Create SaveManager instance
        logger.info("Initializing SaveManager")
        save_manager = SaveManager()
        
        # Verify main save exists and handle initialization errors
        if not save_manager.verify_main_save_exists():
            main_save_path = save_manager.get_main_save_path()
            logger.error(f"Main save file not found at: {main_save_path}")
            error_msg = (
                f"Main save file not found!\n\n"
                f"Expected location:\n{main_save_path}\n\n"
                f"Please ensure Mewgenics has been run at least once to create a save file."
            )
            QMessageBox.critical(None, "Initialization Error", error_msg)
            return 1
        
        # Create MainWindow instance and pass SaveManager to it
        logger.info("Creating main window")
        window = MainWindow(save_manager)
        
        # Load and display initial backup list
        logger.info("Loading initial backup list")
        backups = save_manager.list_backups()
        window.display_backups(backups)
        logger.info(f"Found {len(backups)} backup(s)")
        
        # Show the window
        window.show()
        logger.info("Application window displayed")
        
        # Start Qt event loop
        return app.exec()
        
    except RuntimeError as e:
        # Handle username detection failure
        logger.error(f"Username detection failed: {str(e)}", exc_info=True)
        error_msg = (
            f"Failed to detect Windows username!\n\n"
            f"Error: {str(e)}\n\n"
            f"Please ensure you are running on a Windows system with a valid user account."
        )
        QMessageBox.critical(None, "Initialization Error", error_msg)
        return 1
    
    except Exception as e:
        # Handle any other unexpected initialization errors
        logger.error(f"Unexpected initialization error: {type(e).__name__}: {str(e)}", exc_info=True)
        error_msg = (
            f"An unexpected error occurred during initialization:\n\n"
            f"{type(e).__name__}: {str(e)}"
        )
        QMessageBox.critical(None, "Initialization Error", error_msg)
        return 1


if __name__ == "__main__":
    sys.exit(main())
