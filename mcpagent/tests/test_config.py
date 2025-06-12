import pytest
from pathlib import Path
from mcpagent.application.services.config.manager import ConfigManager
from mcpagent.application.services.config.paths import get_config_dir, get_env_file_path
from mcpagent.application.services.config.fastapi_config import FastAPIConfigModel
from mcpagent.application.services.config.openai_config import OpenAIConfigModel
from mcpagent.application.services.config.langfuse_config import LangfuseConfigModel

def test_config_dir_exists():
    """Test that the config directory exists."""
    config_dir = get_config_dir()
    assert config_dir.exists(), f"Config directory not found at {config_dir}"
    assert config_dir.is_dir(), f"{config_dir} is not a directory"

def test_env_file_exists():
    """Test that the default .env file exists."""
    env_file = get_env_file_path()
    assert env_file.exists(), f"Environment file not found at {env_file}"
    assert env_file.is_file(), f"{env_file} is not a file"

def test_config_manager_initialization():
    """Test that ConfigManager can be initialized."""
    config_manager = ConfigManager()
    assert config_manager is not None

def test_fastapi_config_loading():
    """Test that FastAPI configuration can be loaded."""
    config_manager = ConfigManager()
    fastapi_config = config_manager.get_fastapi_config()
    
    # Test that required fields are loaded
    assert fastapi_config.get_host() is not None
    assert fastapi_config.get_port() is not None
    assert fastapi_config.get_workers() is not None
    assert fastapi_config.get_reload() is not None
    assert fastapi_config.get_access_log() is not None
    assert fastapi_config.get_api_prefix() is not None
    assert fastapi_config.get_api_title() is not None
    assert fastapi_config.get_api_description() is not None
    assert fastapi_config.get_api_version() is not None

def test_openai_config_loading():
    """Test that OpenAI configuration can be loaded."""
    config_manager = ConfigManager()
    openai_config = config_manager.get_openai_config()
    
    # Test that required fields are loaded
    assert openai_config.get_api_key() is not None
    assert openai_config.get_model() is not None
    assert openai_config.get_temperature() is not None

def test_langfuse_config_loading():
    """Test that Langfuse configuration can be loaded."""
    config_manager = ConfigManager()
    langfuse_config = config_manager.get_langfuse_config()
    
    # Test that required fields are loaded
    assert langfuse_config.get_public_key() is not None
    assert langfuse_config.get_secret_key() is not None
    assert langfuse_config.get_host() is not None
    assert langfuse_config.get_timeout() is not None
    assert langfuse_config.get_tags() is not None
    assert langfuse_config.get_version() is not None
    assert langfuse_config.get_release() is not None
    assert langfuse_config.get_environment() is not None

def test_config_caching():
    """Test that configurations are cached."""
    config_manager = ConfigManager()
    
    # Get configurations twice
    config1 = config_manager.get_config(FastAPIConfigModel)
    config2 = config_manager.get_config(FastAPIConfigModel)
    
    # They should be the same instance
    assert config1 is config2

def test_invalid_config_type():
    """Test that invalid configuration types raise an error."""
    config_manager = ConfigManager()
    
    class InvalidConfigModel(FastAPIConfigModel):
        pass
    
    with pytest.raises(ValueError):
        config_manager.get_config(InvalidConfigModel) 