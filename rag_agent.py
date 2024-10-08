#pip install langchain_core,pip install langchain_community,  pip install pypdf, pip install chromadb, pip install langchain_text_splitters
import os

from langchain_community.chat_models import ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.embeddings import HuggingFaceEmbeddings
from fact_checker_agent import check_document_answer

import streamlit as st

template = """<|begin_of_text|><|start_header_id|>system<|end_header_id|>

Given the document and the current conversation between a user and an assistant, your task is as follows: 
answer any user query by using information from the document. Always answer as helpfully as possible, while being safe.
 When the question cannot be answered using the context or document, output the following response: 
 "I cannot answer that question based on the provided document.".

Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. 
Please ensure that your responses are socially unbiased and positive in nature.

If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct.
 If you don't know the answer to a question, please don't share false information.<|eot_id|><|start_header_id|>user<|end_header_id|>

{context}<|eot_id|><|start_header_id|>user<|end_header_id|>

{question}<|eot_id|><|start_header_id|>assistant<|end_header_id|>

"""

llm = ChatOpenAI(
    openai_api_base="https://api.groq.com/openai/v1",
    openai_api_key=os.environ['GROQ_API_KEY'],
    model_name="llama-3.1-70b-versatile",
    temperature=0,
    max_tokens=1000,
)


def load_document():
    print("load_document Start")
    label = "Upload a PDF document here"
    uploaded_file = st.file_uploader(label, type=['pdf'], accept_multiple_files=False, key=None, help=None,
                                     on_change=None,
                                     args=None, kwargs=None, disabled=False, label_visibility="visible")
    documents = None
    if uploaded_file is not None:
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.getbuffer())

        loader = PyPDFLoader("temp.pdf")
        documents = loader.load()
    print("load_document End")
    return documents


def split_documents(documents):
    print("split_documents Start")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=100,
        length_function=len,
        is_separator_regex=False,
    )
    split_documents = None
    if documents:
        split_documents = text_splitter.split_documents(documents)
    print("split_documents End")
    return split_documents


def store_documents(split_documents):
    print("store_documents Start")

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-mpnet-base-v2"
    )

    retriever = None
    if split_documents:
        vectorstore = Chroma.from_documents(documents=split_documents, embedding=embeddings)
        retriever = vectorstore.as_retriever()
    print("store_documents End")
    return retriever


def format_docs(docs):
    return "\n\n".join([d.page_content for d in docs])


def display_questions_answers():
    if 'questions_answers' in st.session_state:
        questions_answers = st.session_state['questions_answers']
        count = 0
        for m in questions_answers:
            if m != "":
                if count % 2 == 0:
                    output = st.chat_message("user")
                    output.write(m)
                else:
                    output = st.chat_message("assistant")
                    output.write(m)
            count += 1


if __name__ == "__main__":
    prompt = ChatPromptTemplate.from_template(template)

    documents = load_document()
    split_docs = split_documents(documents)
    retriever = store_documents(split_docs)

    if retriever:
        chain = (
                {"context": retriever | format_docs, "question": RunnablePassthrough()}
                | prompt
                | llm
                | StrOutputParser()
        )
        st.write(":blue[The document was successfully uploaded. You can start asking questions]")
        question = st.chat_input("Type your questions here")
        if question:
            questions_answers = []
            response = chain.invoke(question)
            result = check_document_answer(question, response)
            if 'questions_answers' not in st.session_state:
                st.session_state['questions_answers'] = questions_answers
            else:
                questions_answers = st.session_state['questions_answers']

            questions_answers.extend([question, result])

        display_questions_answers()
