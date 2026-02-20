"""Logging configuration for Scumgenics Save Manager."""

import logging
import sys
from pathlib import Path
from datetime import datetime


def setup_logging(log_dir: Path = None) -> logging.Logger:
    """
    Set up logging configuration for the application.
    
    Args:
        log_dir: Directory to store log files. Defaults to application directory.
        
    Returns:
        Configured logger instance.
    """
    if log_dir is None:
        log_dir = Path(__file__).parent.parent / "logs"
    
    # Create logs directory if it doesn't exist
    log_dir.mkdir(exist_ok=True)
    
    # Create log filename with timestamp
    log_filename = f"scumgenics_{datetime.now().strftime('%Y%m%d')}.log"
    log_path = log_dir / log_filename
    
    # Configure root logger
    logger = logging.getLogger("scumgenics")
    logger.setLevel(logging.DEBUG)
    
    # Remove existing handlers to avoid duplicates
    logger.handlers.clear()
    
    # File handler - logs everything to file
    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    
    # Console handler - logs warnings and errors to console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.WARNING)
    console_formatter = logging.Formatter("%(levelname)s: %(message)s")
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    logger.info("Logging initialized")
    logger.info(f"Log file: {log_path}")
    
    return logger
