from typing import TypedDict, List
from langchain_core.messages import BaseMessage

class ResearchAgentState(TypedDict):
    messages: List[BaseMessage]
    research_query: str
    search_results: List[str]
    analysis: str
    final_response: str