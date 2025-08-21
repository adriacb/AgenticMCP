from langgraph.graph import MessagesState

class State(MessagesState):
    """State for the graph."""
    prev_node: str
