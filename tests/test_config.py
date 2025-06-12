import os
import pytest
from pathlib import Path
from mcpagent.application.services.config.paths import get_env_file_path
from mcpagent.application.services.config.fastapi_config import FastAPIConfigModel, FastAPIConfig
from mcpagent.application.services.config.openai_config import OpenAIConfigModel, OpenAIConfigImpl
from mcpagent.application.services.config.langfuse_config import LangfuseConfigModel, LangfuseConfigImpl

def test_env_file_exists():
    """Test that the environment file exists."""
    env_file = get_env_file_path("testing")
    assert env_file.exists(), f"Environment file not found at {env_file}"

def test_fastapi_config_loading():
    """Test loading FastAPI configuration."""
    config_model = FastAPIConfigModel.from_env_file(get_env_file_path("testing"))
    config = FastAPIConfig(config_model)
    
    assert config.get_host() == "0.0.0.0"
    assert config.get_port() == 8000
    assert config.get_workers() == 1
    assert config.get_reload() is True
    assert config.get_access_log() is True
    assert config.get_api_prefix() == "/api"
    assert config.get_api_title() == "MCP Agent API"
    assert config.get_api_description() == "API for MCP Agent"
    assert config.get_api_version() == "0.1.0"

def test_openai_config_loading():
    """Test loading OpenAI configuration."""
    config_model = OpenAIConfigModel.from_env_file(get_env_file_path("testing"))
    config = OpenAIConfigImpl(config_model)
    
    assert config.get_api_key() == "test-api-key"
    assert config.get_model() == "gpt-4"
    assert config.get_temperature() == 0.7
    assert config.get_max_tokens() == 1000

def test_langfuse_config_loading():
    """Test loading Langfuse configuration."""
    config_model = LangfuseConfigModel.from_env_file(get_env_file_path("testing"))
    config = LangfuseConfigImpl(config_model)
    
    assert config.get_public_key() == "test-public-key"
    assert config.get_secret_key() == "test-secret-key"
    assert config.get_host() == "https://cloud.langfuse.com"
    assert config.get_timeout() == 30
    assert config.get_tags() == ["environment", "testing"]
    assert config.get_version() == "0.1.0"
    assert config.get_release() == "testing"
    assert config.get_environment() == "testing"

def test_config_caching():
    """Test that configuration is properly cached."""
    config_model1 = FastAPIConfigModel.from_env_file(get_env_file_path("testing"))
    config_model2 = FastAPIConfigModel.from_env_file(get_env_file_path("testing"))
    
    # The models should be equal but not the same object
    assert config_model1 == config_model2
    assert config_model1 is not config_model2 