from langgraph.graph import StateGraph, START, END
from state import AgentState
# Added executor_node import
from agents import supervisor_node, developer_node, qc_node, executor_node 

workflow = StateGraph(AgentState)

workflow.add_node("supervisor", supervisor_node)
workflow.add_node("developer", developer_node)
workflow.add_node("qc", qc_node)
workflow.add_node("executor", executor_node) # ADDED NODE

workflow.add_edge(START, "supervisor")

def router(state: AgentState):
    next_node = state.get("next")
    if next_node == "FINISH":
        return END
    # Added router allowance checkpoint
    elif next_node in ["developer", "qc", "executor"]: 
        return next_node
    return "developer" 

workflow.add_conditional_edges(
    "supervisor",
    router,
    {
        "developer": "developer",
        "qc": "qc",
        "executor": "executor",  # ADDED ROUTE ROADMAP
        END: END
    }
)

workflow.add_edge("developer", "supervisor")
workflow.add_edge("qc", "supervisor")
workflow.add_edge("executor", "supervisor")  # Route back to supervisor to verify run logs

compiled_graph = workflow.compile()