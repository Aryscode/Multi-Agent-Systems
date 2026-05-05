from typing import TypedDict, List
from typing_extensions import Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.types import Send
from langchain_openai import AzureChatOpenAI
from langchain_core.tools import tool
from dotenv import load_dotenv
import operator
from langfuse.langchain import CallbackHandler 
from langfuse import get_client
 

load_dotenv()

# ---- setup langfuse for tracing ----
langfuse = get_client()
langfuse_handler = CallbackHandler()

# ---- Define State ----
class State(TypedDict):
    query: str
    results: Annotated[List[str], operator.add]
    best: str
    tool_call: Annotated[List[dict], operator.add]  # added to pass tool call info

# ---- Calculator tools ----
@tool(description="Add two numbers together")
def add(a: float, b: float) -> float:
    return a + b

@tool(description="Subtract the second number from the first")
def subtract(a: float, b: float) -> float:
    return a - b

@tool(description="Multiply two numbers together")
def multiply(a: float, b: float) -> float:
    return a * b

@tool(description="Divide the first number by the second")
def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

tools = [add, subtract, multiply, divide]

# ---- LLMs ----
llm = AzureChatOpenAI(model="gpt-4o-mini", temperature=0, api_version='2024-08-01-preview', logprobs=True).bind_tools(tools)
judge_llm = AzureChatOpenAI(model="gpt-4o-mini", temperature=0, api_version='2024-08-01-preview')

# ---- Map generator ----
def map_generator(state: State):
    n = 2
    return [Send("agent", {"query": state["query"], "execution_id": i}) for i in range(n)]

# ---- Agent Node ----
def agent_node(state: State) -> State:
    resp = llm.invoke(state["query"])
    # print("Agent LLM response:", resp)

    # If there is a tool call, pass it in state for the tool executor node
    if hasattr(resp, "tool_calls") and resp.tool_calls:
        return {"tool_call": [resp.tool_calls[0]]}  # for simplicity, assume one call
    
    # If no tool call, store LLM content in results
    return {"results": [resp.content], "tool_call": []}

# ---- Tool Executor Node ----
def tool_executor_node(state: State) -> State:
    if not state["tool_call"]:
        return {"results": []}  # No tool call to execute

    tool_call = state["tool_call"][0]  # get first tool call from list
    tool_name = tool_call["name"]
    args = tool_call["args"]

    for t in tools:
        if t.name == tool_name:
            print(f"Executing tool {tool_name} with args {args}")
            # Call the original Python function, not the StructuredTool wrapper
            return {"results": [str(t.func(**args))]}  

    raise ValueError(f"Tool {tool_name} not found")

# ---- Reduce Node ----
def reduce_node(state: State) -> State:
    candidates = state["results"]
    prompt = f"You are a judge. Question: {state['query']}\nCandidates:\n"
    for i, c in enumerate(candidates, 1):
        prompt += f"{i}. {c}\n"
    prompt += "\nPick the single best candidate."
    judgment = judge_llm.invoke(prompt)
    # print("Judge selected:", judgment)
    return {"best": judgment.content}

# ---- Build Workflow ----
workflow = StateGraph(State)
workflow.add_node("agent", agent_node)
workflow.add_node("tool_executor", tool_executor_node)
workflow.add_node("reduce", reduce_node)

workflow.add_conditional_edges(START, map_generator, ["agent"])
workflow.add_edge("agent", "tool_executor")
workflow.add_edge("tool_executor", "reduce")
workflow.add_edge("reduce", END)

app = workflow.compile()
# print(app.get_graph().draw_ascii())

if __name__ == "__main__":
    # final_state = app.invoke({"query": "what is 5 times 80?"})
    # print("\n=== Final Best Response ===")
    # print(final_state["best"])
    for s in app.stream({"query": "what is 5 times 80?"}, config={"callbacks": [langfuse_handler]}):
        print(s)
