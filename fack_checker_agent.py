import os
from langchain.chat_models import ChatOpenAI
from langchain_community.utilities import GoogleSearchAPIWrapper
from langchain.agents import Tool
from langchain.tools.file_management.write import WriteFileTool
from langchain.tools.file_management.read import ReadFileTool
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_experimental.autonomous_agents import BabyAGI
import faiss
from langchain.vectorstores import FAISS





llm = ChatOpenAI(
    openai_api_base="https://api.groq.com/openai/v1",
    openai_api_key=os.environ['GROQ_API_KEY'],
    model_name="llama-3.1-70b-versatile",
    temperature=0,
    max_tokens=1000,
)
search = GoogleSearchAPIWrapper()
tools = [
    Tool(
        name="search",
        func=search.run,
        description="Useful for when you need to answer questions about current events. You should ask targeted questions",
        return_direct=True
    ),
    WriteFileTool(),
    ReadFileTool(),
]

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2"
)
embedding_size = 1536

index = faiss.IndexFlatL2(embedding_size)
vectorstore = FAISS(embeddings.embed_query, index, InMemoryDocstore({}), {})

agent = baby_agi = BabyAGI.from_llm(
    ai_name="Jim",
    ai_role="Assistant",
    tools=tools,
    llm=llm,
    vectorstore=vectorstore
)


def check_document_answer(question, answer):
    print(question, "*******************************")
    print(answer, "*******************************")

    prompt = f"""
                    Given the user query '{question}' and the assistant's response '{answer}', perform the following tasks:
    
                    Utilize your search capabilities to verify the accuracy of the provided answer.
                    Evaluate the credibility of sources used to determine the accuracy.
                    RETURN A RESPONSE CONTAINING:
    
                    a. The document answer.
                    b. A verification statement (Accurate/Partially Accurate/Inaccurate).
                    c. If necessary, provide a corrected or more accurate answer.
                    d. Briefly explain the reasoning behind your verification (optional).
                    Ensure your response prioritizes factual accuracy, clarity, and conciseness. 
             """
    result = llm.invoke(prompt)
    print(result.content)
    return result.content
