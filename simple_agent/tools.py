import os
from dotenv import load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.tools import ArxivQueryRun
from langchain_community.utilities import ArxivAPIWrapper
# from langchain_core.tools import tool


load_dotenv()

# Initialize Tavily search tool
search_tool = TavilySearchResults(
    max_results=3,
    tavily_api_key=os.getenv("TAVILY_API_KEY"),
)
# Initialize Arxiv tool
arxiv = ArxivAPIWrapper(
    top_k_results=3,
    sort_by="relevancy",
    sort_order="descending"
)
arxiv_tool = ArxivQueryRun(api_wrapper=arxiv)
