"""
Utility functions for BuyerScout.
Includes logging setup, file I/O helpers, and common utilities.
"""

import logging
import os
import json
import csv
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

from config import config


def setup_logging(log_level: str = "INFO", log_file: Optional[str] = None) -> logging.Logger:
    """
    Configure application-wide logging.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional path to log file. If None, uses default from config
    
    Returns:
        Configured logger instance
    """
    # Create logs directory if it doesn't exist
    log_dir = Path(config.LOGS_PATH)
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Default log file name with timestamp
    if log_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = log_dir / f"buyerscout_{timestamp}.log"
    
    # Configure logging format
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
    
    # Setup logging configuration
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format=log_format,
        datefmt=date_format,
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()  # Also log to console
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info(f"Logging initialized. Log file: {log_file}")
    
    return logger


def save_to_csv(data: List[Dict], filepath: str, mode: str = "w") -> bool:
    """
    Save a list of dictionaries to a CSV file.
    
    Args:
        data: List of dictionaries to save
        filepath: Path to output CSV file
        mode: File mode ('w' for write, 'a' for append)
    
    Returns:
        True if successful, False otherwise
    """
    if not data:
        return False
    
    try:
        # Ensure directory exists
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        
        # Get all unique keys from all dictionaries
        fieldnames = set()
        for item in data:
            fieldnames.update(item.keys())
        fieldnames = sorted(list(fieldnames))
        
        with open(filepath, mode, newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # Write header only if in write mode
            if mode == 'w':
                writer.writeheader()
            
            writer.writerows(data)
        
        return True
    except Exception as e:
        logging.error(f"Error saving CSV to {filepath}: {e}")
        return False


def save_to_json(data: List[Dict], filepath: str, indent: int = 2) -> bool:
    """
    Save a list of dictionaries to a JSON file.
    
    Args:
        data: List of dictionaries to save
        filepath: Path to output JSON file
        indent: JSON indentation level
    
    Returns:
        True if successful, False otherwise
    """
    try:
        # Ensure directory exists
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as jsonfile:
            json.dump(data, jsonfile, indent=indent, ensure_ascii=False)
        
        return True
    except Exception as e:
        logging.error(f"Error saving JSON to {filepath}: {e}")
        return False


def load_from_json(filepath: str) -> Optional[List[Dict]]:
    """
    Load data from a JSON file.
    
    Args:
        filepath: Path to JSON file
    
    Returns:
        List of dictionaries, or None if error
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as jsonfile:
            return json.load(jsonfile)
    except Exception as e:
        logging.error(f"Error loading JSON from {filepath}: {e}")
        return None


def ensure_data_directories():
    """Ensure all data directories exist."""
    Path(config.DATA_RAW_PATH).mkdir(parents=True, exist_ok=True)
    Path(config.DATA_PROCESSED_PATH).mkdir(parents=True, exist_ok=True)
    Path(config.LOGS_PATH).mkdir(parents=True, exist_ok=True)

