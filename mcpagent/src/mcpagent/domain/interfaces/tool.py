from abc import ABC, abstractmethod

class ToolInterface(ABC):
    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def get_description(self) -> str:
        pass
    
    @abstractmethod
    def get_arguments(self) -> dict:
        pass
