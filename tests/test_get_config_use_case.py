import pytest
from mcpagent.application.use_cases.get_config_use_case import GetConfigUseCase

def test_get_config_use_case():
    """Test getting configurations through the use case."""
    use_case = GetConfigUseCase(env="testing")
    
    # Test FastAPI config
    fastapi_config = use_case.get_fastapi_config()
    assert fastapi_config.get_host() == "0.0.0.0"
    assert fastapi_config.get_port() == 8000
    assert fastapi_config.get_workers() == 1
    assert fastapi_config.get_reload() is True
    assert fastapi_config.get_access_log() is True
    assert fastapi_config.get_api_prefix() == "/api"
    assert fastapi_config.get_api_title() == "MCP Agent API"
    assert fastapi_config.get_api_description() == "API for MCP Agent"
    assert fastapi_config.get_api_version() == "0.1.0"
    
    # Test OpenAI config
    openai_config = use_case.get_openai_config()
    assert openai_config.get_api_key() == "test-api-key"
    assert openai_config.get_model() == "gpt-4"
    assert openai_config.get_temperature() == 0.7
    assert openai_config.get_max_tokens() == 1000
    
    # Test Langfuse config
    langfuse_config = use_case.get_langfuse_config()
    assert langfuse_config.get_public_key() == "test-public-key"
    assert langfuse_config.get_secret_key() == "test-secret-key"
    assert langfuse_config.get_host() == "https://cloud.langfuse.com"
    assert langfuse_config.get_timeout() == 30
    assert langfuse_config.get_tags() == ["environment", "testing"]
    assert langfuse_config.get_version() == "0.1.0"
    assert langfuse_config.get_release() == "testing"
    assert langfuse_config.get_environment() == "testing"

def test_config_caching():
    """Test that configurations are properly cached."""
    use_case = GetConfigUseCase(env="testing")
    
    # Get configs twice
    fastapi_config1 = use_case.get_fastapi_config()
    fastapi_config2 = use_case.get_fastapi_config()
    
    openai_config1 = use_case.get_openai_config()
    openai_config2 = use_case.get_openai_config()
    
    langfuse_config1 = use_case.get_langfuse_config()
    langfuse_config2 = use_case.get_langfuse_config()
    
    # Configs should be the same object (cached)
    assert fastapi_config1 is fastapi_config2
    assert openai_config1 is openai_config2
    assert langfuse_config1 is langfuse_config2 