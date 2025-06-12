from mcpagent.domain.interfaces.tool import ToolInterface

class Tool(ToolInterface):
    def __init__(self, name: str, description: str, parameters: dict):
        self.name = name
        self.description = description
        self.parameters = parameters

    def get_name(self) -> str:
        return self.name

    def get_description(self) -> str:
        return self.description 

    def get_parameters(self) -> dict:
        return self.parameters
