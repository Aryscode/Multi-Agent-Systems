from typing import List, TypedDict

class AgentState(TypedDict):
    task: str
    plan: str
    steps: List[str]
    results: dict
    final_answer: str

