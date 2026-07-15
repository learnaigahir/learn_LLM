from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    # 'add_messages' ensures new messages append to the history list rather than overwriting it
    messages: Annotated[Sequence[BaseMessage], add_messages]
    # Track the next active worker node in the system
    next: str
    # Holds intermediate artifacts such as raw code strings or test results
    current_code: str
    qc_report: str
    execution_output: str
