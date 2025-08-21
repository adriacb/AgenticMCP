import structlog
import logging
import sys
from typing import Optional, Any, List
from dataclasses import dataclass

@dataclass
class LoggerConfig:
    """Configuration class for structlog logger settings."""
    level: str = "INFO"
    json_format: bool = False
    processors: Optional[List[Any]] = None
    context_class: Optional[Any] = None
    wrapper_class: Optional[Any] = None
    cache_logger_on_first_use: bool = True
    logger_factory: Optional[Any] = None
    additional_processors: Optional[List[Any]] = None

    def get_processors(self) -> List[Any]:
        """Get the list of processors based on configuration."""
        processors = [
            structlog.contextvars.merge_contextvars,  # Add contextvars processor first
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
        ]

        # Add additional processors before the renderer
        if self.additional_processors:
            processors.extend(self.additional_processors)

        # Add the renderer last
        if self.json_format:
            processors.append(structlog.processors.JSONRenderer())
        else:
            processors.append(structlog.dev.ConsoleRenderer())

        return processors

class LoggerInitializer:
    """Class for initializing and configuring structlog logger."""
    
    @staticmethod
    def initialize(config: LoggerConfig) -> structlog.BoundLogger:
        """Initialize and configure structlog logger with the given configuration."""
        # Ensure root logger and handlers use the requested level.
        level_name = str(config.level).upper()
        level = getattr(logging, level_name, logging.INFO)
        root = logging.getLogger()
        # add a default StreamHandler only if no handlers exist
        if not root.handlers:
            handler = logging.StreamHandler(sys.stdout)
            handler.setFormatter(logging.Formatter("%(message)s"))
            root.addHandler(handler)
        # set level on root and all handlers (forces update on re-init)
        root.setLevel(level)
        for h in root.handlers:
            h.setLevel(level)

        # Configure structlog
        structlog.configure(
            processors=config.get_processors(),
            wrapper_class=config.wrapper_class or structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=config.cache_logger_on_first_use,
            logger_factory=config.logger_factory or structlog.stdlib.LoggerFactory(),
        )

        # Clear any existing context
        structlog.contextvars.clear_contextvars()

        # Get the logger
        return structlog.get_logger()

    @staticmethod
    def get_default_logger() -> structlog.BoundLogger:
        """Get a logger with default configuration."""
        default_config = LoggerConfig()
        return LoggerInitializer.initialize(default_config)


