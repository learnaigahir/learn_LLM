from langchain_core.messages import HumanMessage
from graph import compiled_graph

def run_multi_agent_system(user_prompt: str):
    print(f"Initializing request: {user_prompt}\n" + "="*50)
    
    initial_state = {
        "messages": [HumanMessage(content=user_prompt)],
        "current_code": "",
        "qc_report": "",
        "execution_output": "",  # Make sure this is initialized
        "next": "supervisor"
    }
    
    config = {"recursion_limit": 30}
    
    try:
        for event in compiled_graph.stream(initial_state, config=config):
            for node_name, output in event.items():
                print(f"\n[Actor Node: {node_name.upper()}]")
                
                # Print message text from agents
                if "messages" in output and output["messages"]:
                    raw_content = output["messages"][-1].content
                    if isinstance(raw_content, list):
                        text_parts = [part if isinstance(part, str) else part.get("text", "") for part in raw_content]
                        last_msg = "".join(text_parts)
                    else:
                        last_msg = str(raw_content)
                    print(last_msg[:600] + ("..." if len(last_msg) > 600 else ""))
                
                # PRINT DYNAMIC CODES EXECUTION DOCK HERE
                if "execution_output" in output and output["execution_output"]:
                    print(f"\n[CONSOLE RUN OUTPUT]:")
                    print(output["execution_output"])
                    
                if "next" in output:
                    print(f"Decision: Next routing destination -> {output['next']}")
                print("-" * 40)
    except Exception as e:
        print(f"\nGraph execution halted: {e}")

if __name__ == "__main__":
    # Test with a completely different project!
    task = (
        "Develop a lightweight signup page which will host/launch in local. The signup page will ask username, email id, phone number, gender, country. Once user input the information. It will have submit and cancel button. Once user submit, it will close the sign up window. If user cancel it will reset the text boxes"
        "Intentionally include only one typo in the code calculation logic so the QC agent "
        "has to catch it and trigger a revision. once QC passed, launch or trigger developed app/project"
    )
    run_multi_agent_system(task)