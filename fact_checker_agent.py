import os
from langchain.chat_models import ChatOpenAI


llm = ChatOpenAI(
    openai_api_base="https://api.groq.com/openai/v1",
    openai_api_key=os.environ['GROQ_API_KEY'],
    model_name="llama-3.1-70b-versatile",
    temperature=0,
    max_tokens=1000,
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
