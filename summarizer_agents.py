#pip install newspaper3k
from langchain_community.chat_models import ChatOpenAI
from langchain_community.tools import Tool, DuckDuckGoSearchResults
from langchain.agents import initialize_agent, AgentType
from tools import CustomWebScraperTool

import os

llm = ChatOpenAI(
    openai_api_base="https://api.groq.com/openai/v1",
    openai_api_key=os.environ['GROQ_API_KEY'],
    model_name="llama-3.1-70b-versatile",
    temperature=0,
    max_tokens=1000,
)


def get_research_agent():
    search = DuckDuckGoSearchResults()
    search_tools = [
        Tool(
            name="search",
            func=search.run,
            description="Search DuckDuckGo for recent results.",
            return_direct=True
        ),
    ]

    research_agent = initialize_agent(
        tools=search_tools,
        agent_type=AgentType.SELF_ASK_WITH_SEARCH,
        llm=llm,
        handle_parsing_errors=True,
        verbose=True
    )
    return research_agent


def get_writer_agent():
    scraper = CustomWebScraperTool()
    writing_tools = [
        Tool(
            name=scraper.name,
            func=scraper.run,
            description=scraper.description
        ),
    ]

    agent = initialize_agent(
        tools=writing_tools,
        agent_type=AgentType.SELF_ASK_WITH_SEARCH,
        llm=llm,
        handle_parsing_errors=True,
        verbose=True
    )
    return agent
