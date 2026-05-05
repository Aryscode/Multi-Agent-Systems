# main.py
import os
from dotenv import load_dotenv
from typing import Literal

from langgraph.graph import StateGraph, END

from agent_state import AgentState
from tools import search_tool, arxiv_tool
from graph_nodes import planner, tool_executor_chain, answer_chain

from langfuse import Langfuse, observe

langfuse = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv("LANGFUSE_HOST")
)

# Load environment variables
load_dotenv()
os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")

# --- Node Functions ---
@observe()
def plan_step(state: AgentState):
    """Generates the initial research plan."""
    print("---PLANNING---")
    plan = planner.invoke({"task": state["task"]})
    return {"plan": plan, "steps": []}

@observe()
def tool_step(state: AgentState):
    """Executes a tool based on the current plan."""
    print("---EXECUTING TOOL---")
    current_steps = state.get("steps", [])


    tool_choice = tool_executor_chain.invoke(
        {"plan": state["plan"], "steps": state["steps"]}
    )
    
    # Execute the appropriate tool based on the tool choice
    if tool_choice.tool_name == "arxiv":
        result = arxiv_tool.invoke(tool_choice.tool_input)
    else:
        result = search_tool.invoke(tool_choice.tool_input)
    
    # Update state
    new_steps = current_steps + [f"Called tool '{tool_choice.tool_name}' with input '{tool_choice.tool_input}'"]
    new_results = state.get("results", {})
    if tool_choice.tool_name not in new_results:
        new_results[tool_choice.tool_name] = []
    new_results[tool_choice.tool_name].append(result)

    return {"steps": new_steps, "results": new_results}

@observe()
def answer_step(state: AgentState):
    """Generates the final answer."""
    print("---GENERATING FINAL ANSWER---")
    final_answer = answer_chain.invoke({
        "task": state["task"],
        "results": str(state["results"])
    })
    return {"final_answer": final_answer}

# --- Conditional Edge Logic ---
@observe()
def should_continue(state: AgentState) -> Literal["continue", "end"]:
    """Determines whether to continue planning or end."""

    if len(state["steps"]) == 0:
        return "continue"
    else:
        return "end"

# --- Define the Graph ---
graph = StateGraph(AgentState)

# Add nodes
graph.add_node("planner", plan_step)
graph.add_node("tool_executor", tool_step)
graph.add_node("final_answer_generator", answer_step)

# Set the entry point
graph.set_entry_point("planner")

# Add edges
graph.add_edge("planner", "tool_executor")
graph.add_edge("final_answer_generator", END)

# Add conditional edge
graph.add_conditional_edges(
    "tool_executor",
    should_continue,
    {
        "continue": "planner",  # A more complex agent would loop back to re-plan
        "end": "final_answer_generator"
    }
)

# Compile the graph
app = graph.compile()

# --- Run the Agent ---
if __name__ == "__main__":
    task = {"task": "What are the latest advancements in AI-powered drug discovery?"}
    print("Starting the agent...\n")
    for event in app.stream(task):
        for key, value in event.items():
            print(f"Node '{key}' output:")
            print("---")
            print(value)
        print("\n=====================\n")
