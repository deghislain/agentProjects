import os
from langchain.chat_models import ChatOpenAI
from langchain.agents import Tool, initialize_agent, AgentType
from langchain.utilities import GoogleSearchAPIWrapper
from langchain_experimental.utilities import PythonREPL


llm = ChatOpenAI(
    openai_api_base="https://api.groq.com/openai/v1",
    openai_api_key=os.environ['GROQ_API_KEY'],
    model_name="llama-3.1-70b-versatile",
    temperature=0,
    max_tokens=1000,
)

search = GoogleSearchAPIWrapper()
python_repl = PythonREPL()

tools = [
    Tool(
        name="google-search",
        func=search.run,
        description="useful for when you need to search Google to answer questions about current events"
    ),
    Tool(
        name="python_repl",
        description="A Python shell. Use this to execute Python commands. Input should be a valid Python command. Useful for saving strings to files.",
        func=python_repl.run
    )
]

agent = initialize_agent(
        tools=tools,
        agent_type=AgentType.SELF_ASK_WITH_SEARCH,
        llm=llm,
        handle_parsing_errors=True,
        verbose=True
    )


def check_document_answer(question, answer):
    print(question, "*******************************")
    print(answer, "*******************************")

    prompt = f"""
                     Given the following question {question} verify the accuracy of {answer} Using the content of 'search_response.txt'
                     and your search capabilities.
                     Assess the credibility of sources used to determine the accuracy.
                     Provide a Response Containing:
            
                       a. Assistant's Response: Repeat the original answer.
                       b. Verification Statement: (Accurate/Partially Accurate/Inaccurate).
                       c. Corrected/More Accurate Answer (if necessary): Provide an updated response.
                       d. Verification Rationale (optional): Briefly explain the reasoning behind your verification.
            
                    Prioritize:
                    
                        Factual accuracy
                        Clarity
                        Conciseness
             """

    response = agent.run(f"Find the answer to this question {question} and save it to a file 'search_response.txt'.")
    print("search_response***************** ", response)


    agent_resp = agent.run(prompt)
    print("agent_resp----------------------", agent_resp)
    return agent_resp
