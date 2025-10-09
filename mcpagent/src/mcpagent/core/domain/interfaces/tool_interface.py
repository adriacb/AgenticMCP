from abc import ABC, abstractmethod


class ToolInterface(ABC):
    """
    Abstract base class for tools that can be used by the agent.
    """

    @abstractmethod
    def execute(self, *args, **kwargs):
        """
        Execute the tool's functionality with the provided arguments.
        """
        pass
