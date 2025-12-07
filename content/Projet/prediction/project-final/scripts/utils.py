"""
Utility Functions
Common utilities for the BDA project
"""

import os
import yaml
from datetime import datetime


def load_config(config_path="bda_project_config.yml"):
    """
    Load project configuration from YAML file.
    
    Args:
        config_path: Path to config file
    
    Returns:
        dict: Configuration dictionary
    """
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config


def ensure_dir(directory):
    """
    Create directory if it doesn't exist.
    
    Args:
        directory: Path to directory
    """
    os.makedirs(directory, exist_ok=True)


def get_timestamp():
    """
    Get current timestamp in ISO format.
    
    Returns:
        str: Timestamp string
    """
    return datetime.now().isoformat()


def log_message(message, level="INFO"):
    """
    Log a message with timestamp.
    
    Args:
        message: Message to log
        level: Log level (INFO, WARN, ERROR)
    """
    timestamp = get_timestamp()
    print(f"[{timestamp}] [{level}] {message}")


def save_text_to_file(text, filepath):
    """
    Save text content to file.
    
    Args:
        text: Text content
        filepath: Output file path
    """
    ensure_dir(os.path.dirname(filepath))
    with open(filepath, 'w') as f:
        f.write(text)
    log_message(f"Saved to: {filepath}")


def append_to_csv(data, filepath, header=None):
    """
    Append data to CSV file.
    
    Args:
        data: List of values or dict
        filepath: CSV file path
        header: CSV header (list) if file doesn't exist
    """
    ensure_dir(os.path.dirname(filepath))
    
    file_exists = os.path.exists(filepath)
    
    with open(filepath, 'a') as f:
        # Write header if file doesn't exist
        if not file_exists and header:
            f.write(','.join(header) + '\n')
        
        # Write data
        if isinstance(data, dict):
            f.write(','.join(str(v) for v in data.values()) + '\n')
        elif isinstance(data, list):
            f.write(','.join(str(v) for v in data) + '\n')
        else:
            f.write(str(data) + '\n')


def format_bytes(bytes_size):
    """
    Format bytes to human-readable string.
    
    Args:
        bytes_size: Size in bytes
    
    Returns:
        str: Formatted string (e.g., "1.5 GB")
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} PB"


def format_duration(seconds):
    """
    Format duration in seconds to human-readable string.
    
    Args:
        seconds: Duration in seconds
    
    Returns:
        str: Formatted string (e.g., "1h 23m 45s")
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    
    parts = []
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if secs > 0 or not parts:
        parts.append(f"{secs}s")
    
    return ' '.join(parts)


def validate_file_exists(filepath):
    """
    Validate that a file exists.
    
    Args:
        filepath: Path to file
    
    Raises:
        FileNotFoundError: If file doesn't exist
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")


def validate_directory_exists(directory):
    """
    Validate that a directory exists.
    
    Args:
        directory: Path to directory
    
    Raises:
        NotADirectoryError: If directory doesn't exist
    """
    if not os.path.isdir(directory):
        raise NotADirectoryError(f"Directory not found: {directory}")


def get_file_size(filepath):
    """
    Get file size in bytes.
    
    Args:
        filepath: Path to file
    
    Returns:
        int: File size in bytes
    """
    return os.path.getsize(filepath)


def list_files_in_directory(directory, extension=None):
    """
    List all files in a directory.
    
    Args:
        directory: Path to directory
        extension: Filter by extension (e.g., '.csv')
    
    Returns:
        list: List of file paths
    """
    files = []
    for root, dirs, filenames in os.walk(directory):
        for filename in filenames:
            if extension is None or filename.endswith(extension):
                files.append(os.path.join(root, filename))
    return files


if __name__ == "__main__":
    # Test utilities
    print("Testing utility functions...")
    
    config = load_config()
    print(f"Loaded config: {list(config.keys())}")
    
    print(f"Current timestamp: {get_timestamp()}")
    print(f"Format 1536 bytes: {format_bytes(1536)}")
    print(f"Format 3665 seconds: {format_duration(3665)}")
    
    print("Utility functions working correctly!")
