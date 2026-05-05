import os
from dotenv import load_dotenv
from langchain_tavily import TavilySearch

import warnings

warnings.filterwarnings("ignore", category=UserWarning)
load_dotenv()

search_tool = TavilySearch(
    max_results=3,
    tavily_api_key=os.getenv("TAVILY_API_KEY")
)

print(search_tool.invoke({"query": "What happened at the last wimbledon"}))

