#pip install newspaper3k
from langchain_community.chat_models import ChatOpenAI
import summarizer_agents as agents
import summarizer_prompts as prompt
import utilities as util
import os
import streamlit as st
import pdf_generator as pdf
from file_path import PATH_TO_GENERATED_CONTENT

llm = ChatOpenAI(
    openai_api_base="https://api.groq.com/openai/v1",
    openai_api_key=os.environ['GROQ_API_KEY'],
    model_name="llama-3.1-70b-versatile",
    temperature=0,
    max_tokens=1000,
)

if __name__ == "__main__":
    topic = st.text_input(":blue[Research Topic]")
    links = st.text_area(":blue[Additional sources to consider]", placeholder="Paste your links here")

    # here we create the 3 columns needed for the button e.g Start Research
    left, middle, right = st.columns(3)

    if left.button("Start Research", key="leftbt"):
        if topic:
            search_prompt = prompt.get_search_prompt(topic)
            search_agent = agents.get_research_agent()
            search_result = search_agent.run(search_prompt)
            sources = util.extract_sources(search_result, links)

            write_prompt = prompt.get_write_prompt(topic, sources)
            writer_agent = agents.get_writer_agent()
            generated_content = writer_agent.run(write_prompt)

            if generated_content:
                right.button("Export as pdf", key="rightbt", on_click=pdf.generate_pdf, args=[topic])
                util.store_the_content(topic, generated_content, PATH_TO_GENERATED_CONTENT)
                st.write(generated_content)
