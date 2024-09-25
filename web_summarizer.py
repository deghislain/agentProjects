#pip install newspaper3k
from langchain_community.chat_models import ChatOpenAI
import summarizer_agents as agents
import summarizer_prompts as prompt
import re
import os
import streamlit as st


llm = ChatOpenAI(
    openai_api_base="https://api.groq.com/openai/v1",
    openai_api_key=os.environ['GROQ_API_KEY'],
    model_name="llama-3.1-70b-versatile",
    temperature=0,
    max_tokens=1000,
)


def extract_sources(text, links):
    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    urls = re.findall(url_pattern, text)
    urls + re.findall(url_pattern, links)
    return urls


if __name__ == "__main__":
    topic = st.text_input(":blue[Research Topic]")
    links = st.text_area(":blue[Additional sources to consider]", placeholder="Paste your links here")
    if topic:
        search_prompt = prompt.get_search_prompt(topic)
        search_agent = agents.get_research_agent()
        search_result = search_agent.run(search_prompt)
        sources = extract_sources(search_result, links)
        write_prompt = prompt.get_write_prompt(topic, sources)

        writer_agent = agents.get_writer_agent()
        generated_content = writer_agent.run(write_prompt)
        st.write(generated_content)
