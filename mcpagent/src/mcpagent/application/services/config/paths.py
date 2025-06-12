from pathlib import Path
import os

def get_project_root() -> Path:
    """Get the project root directory.
    
    Returns:
        Path: The project root directory.
    """
    
    return Path(__file__).parent.parent.parent.parent.parent.parent

def get_config_dir() -> Path:
    """Get the configuration directory.
    
    Returns:
        Path: The configuration directory.
    """
    return get_project_root() / "config"

def get_env_file_path(env: str = "development") -> Path:
    """Get the path to the environment file.
    
    Args:
        env: The environment name (e.g., 'development', 'production', 'testing').
        
    Returns:
        Path: The path to the environment file.
    """
    return get_config_dir() / f".env.{env}"

def get_default_env_file_path() -> Path:
    """Get the path to the default environment file.
    
    Returns:
        Path: The path to the default environment file.
    """
    return get_config_dir() / ".env" 