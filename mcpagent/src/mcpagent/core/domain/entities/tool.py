from mcpagent.core.domain.interfaces import ToolInterface
from mcpagent.core.domain.value_objects import ToolCard


class Tool(ToolInterface):
    """
    Represents a tool that can be used by an agent.
    """
    def __init__(self, 
                 tool_card: ToolCard
                 ):
        self.name = tool_card.name
        self.description = tool_card.description
        self.tags = tool_card.tags
        self.examples = tool_card.examples
        self.parameters = tool_card.parameters
        self.function = tool_card.function
        self.args_schema = tool_card.args_schema
        
    def execute(self, *args, **kwargs):
        """
        Execute the tool with the given arguments.
        """
        return self.function(
            *args, 
            **kwargs
            )
    
    def __repr__(self):
        return f"Tool(name={self.name}, description={self.description}, tags={self.tags}, examples={self.examples})"