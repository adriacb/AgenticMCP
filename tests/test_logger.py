import pytest
import structlog
from mcpagent.application.services.logger import LoggerConfig, LoggerInitializer

def test_logger_config_defaults():
    """Test LoggerConfig with default values."""
    config = LoggerConfig()
    assert config.level == "INFO"
    assert config.json_format is False
    assert config.cache_logger_on_first_use is True
    assert config.processors is None
    assert config.context_class is None
    assert config.wrapper_class is None
    assert config.logger_factory is None
    assert config.additional_processors is None

def test_logger_config_custom_values():
    """Test LoggerConfig with custom values."""
    config = LoggerConfig(
        level="DEBUG",
        json_format=True,
        cache_logger_on_first_use=False
    )
    assert config.level == "DEBUG"
    assert config.json_format is True
    assert config.cache_logger_on_first_use is False

def test_logger_config_processors():
    """Test LoggerConfig processor generation."""
    config = LoggerConfig()
    processors = config.get_processors()
    
    # Check that essential processors are present
    assert any(p.__name__ == "merge_contextvars" for p in processors)
    assert any(p is structlog.stdlib.add_log_level for p in processors)
    assert any(isinstance(p, structlog.stdlib.PositionalArgumentsFormatter) for p in processors)
    assert any(isinstance(p, structlog.processors.TimeStamper) for p in processors)
    assert any(isinstance(p, structlog.processors.StackInfoRenderer) for p in processors)
    assert any(p is structlog.processors.format_exc_info for p in processors)
    
    # Check that ConsoleRenderer is the last processor when json_format is False
    assert isinstance(processors[-1], structlog.dev.ConsoleRenderer)

def test_logger_config_json_format():
    """Test LoggerConfig with JSON format."""
    config = LoggerConfig(json_format=True)
    processors = config.get_processors()
    assert isinstance(processors[-1], structlog.processors.JSONRenderer)

def test_logger_initializer_default():
    """Test LoggerInitializer with default configuration."""
    logger = LoggerInitializer.get_default_logger()
    assert hasattr(logger, "info")  # Check for logger methods instead of type
    assert hasattr(logger, "error")
    assert hasattr(logger, "debug")
    
    # Test logging
    logger.info("test message", test_key="test_value")
    # Note: We can't easily test the output format without capturing stdout
    # The actual output verification would require more complex test setup

def test_logger_initializer_custom():
    """Test LoggerInitializer with custom configuration."""
    config = LoggerConfig(
        level="DEBUG",
        json_format=True
    )
    logger = LoggerInitializer.initialize(config)
    assert hasattr(logger, "info")  # Check for logger methods instead of type
    assert hasattr(logger, "error")
    assert hasattr(logger, "debug")
    
    # Test logging with context
    logger = logger.bind(test_context="value")
    logger.info("test message", test_key="test_value")
    # Note: We can't easily test the output format without capturing stdout
    # The actual output verification would require more complex test setup 