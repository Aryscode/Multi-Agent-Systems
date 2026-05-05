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
from langfuse import observe
 

load_dotenv()

# ---- setup langfuse for tracing ----
langfuse = get_client()
langfuse_handler = CallbackHandler()

# ---- Define State ----
class State(TypedDict):
    query: str  # The input query
    agent_response: Annotated[List[dict], operator.add]  # List of agent responses
    best: str  # The final best result

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

    # Execute any requested tool calls
    if hasattr(resp, "tool_calls") and resp.tool_calls:
        tool_results = []

        for tc in resp.tool_calls:
            result = tool_executor(tc)
            tool_results.append(str(result))  # Convert to string for aggregation
    else:
        tool_results = None
    
    return {"agent_response": [{"llm_response":resp,"tool_results": tool_results}]}

# ---- Tool Executor ----
# @observe()
def tool_executor(tool_call) -> any:
    """
    Executes a tool call object from the LLM.
    tool_call: {'name': 'multiply', 'args': {'a':5,'b':80}, ...}
    """
    tool_name = tool_call["name"]
    args = tool_call["args"]

    for t in tools:
        if t.name == tool_name:
            return "result of " + tool_name + " with arguments " + str(args) + " is " + str(t.func(**args)) 

    
    raise ValueError(f"Tool {tool_name} not found")

# ---- Reduce Node ----
def reduce_node(state: State) -> State:
    candidates = state["agent_response"]
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
workflow.add_node("reduce", reduce_node)

workflow.add_conditional_edges(START, map_generator, ["agent"])
workflow.add_edge("agent", "reduce")
workflow.add_edge("reduce", END)

app = workflow.compile()
# print(app.get_graph().draw_ascii())

if __name__ == "__main__":
    query = "what is 5 times 80 and 18th of 90?"
    # query = "what are AI agents?"
    for s in app.stream({"query": query}, config={"callbacks": [langfuse_handler]}):
        print(s)
