import operator
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.output_parsers.string import StrOutputParser

llm = ChatOllama(model="qwen2.5:7b", base_url="http://localhost:11434", temperature=0)

# 1. Plannning Node
planner_prompt = ChatPromptTemplate.from_template(
    """Create a step-by-step plan to research the following user query. 
    Your plan should be a short list of simple, actionable steps. Nothing should be there apart from list. 

    Query: {task}"""
)
planner = planner_prompt | llm | StrOutputParser()

# 2. Tool Execution Node
class ToolExecutor(BaseModel):
    """Tool execution schema."""
    tool_name: str = Field(description="The name of the tool to execute.")
    tool_input: str = Field(description="The input to pass to the tool.")

# Set up a PydanticOutputParser
parser = PydanticOutputParser(pydantic_object=ToolExecutor)

tool_executor_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", 
         '''You are an expert at choosing the correct tool and input to answer a user's question. 
         Return a JSON object that matches the following Pydantic model:

         class ToolExecutor(BaseModel):
             tool_name: str  # Must be either "tavily_search" for web search or "arxiv" for academic papers
             tool_input: str  # The search query to use
         
         Choose "arxiv" when the query is specifically about academic research, scientific papers, or technical publications.
         Choose "tavily_search" for general web searches and current information.'''),
        ("user", "Based on the following plan, what is the next tool to call and what is its input?\n\nPlan:\n{plan}\n\nCompleted Steps:\n{steps}"),
    ]
)

# tool_executor_prompt = ChatPromptTemplate.from_messages(
#     [
#         ("system", "You are an expert at choosing the correct tool and input to answer a user's question."),
#         ("user", "Based on the following plan, what is the next tool to call and what is its input?\n\nPlan:\n{plan}\n\nCompleted Steps:\n{steps}"),
#     ]
# )
tool_executor_chain = tool_executor_prompt | llm | parser

# 3. Final Answer Node
answer_prompt = ChatPromptTemplate.from_template(
    """Based on the original query and the research results, provide a comprehensive final answer.

    Query: {task}

    Research Results:
    {results}
    """
)
answer_chain = answer_prompt | llm | StrOutputParser()