import os
import streamlit as st
import random
import time
import re
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.retrievers import MultiQueryRetriever
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage, AIMessage
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import pandas as pd
from streamlit_feedback import streamlit_feedback
from secret_key import my_openapi_key

# Securely set up environment variables for API keys
os.environ['OPENAI_API_KEY'] = my_openapi_key


# Helper functions
def get_pdf_text(pdf_paths):
    text = ""
    for pdf_path in pdf_paths:
        pdf_reader = PdfReader(pdf_path)
        for page in pdf_reader.pages:
            text += page.extract_text()
    cleaned_text = re.sub(r'\s+', ' ', text)  # Replace multiple whitespace with a single space
    return cleaned_text

def get_text_chunks_with_metadata(text, source, page_number=None):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=100)
    chunks = text_splitter.split_text(text)
    chunk_metadata = [{"source": source, "page_number": page_number, "chunk_index": i} for i, chunk in enumerate(chunks)]
    return list(zip(chunks, chunk_metadata))

def get_vectorstore(text_chunks_with_metadata):
    embeddings = OpenAIEmbeddings()
    texts = [text for text, metadata in text_chunks_with_metadata]
    metadatas = [metadata for text, metadata in text_chunks_with_metadata]
    vectorstore = FAISS.from_texts(texts=texts, embedding=embeddings, metadatas=metadatas)
    return vectorstore

def get_conversation_chain(vectorstore):
    llm = ChatOpenAI(temperature=0)
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    QUERY_PROMPT = PromptTemplate(template="You are a churchill car insurance provider agent. Your task is to generate five different versions of the given user {question} to retrieve relevant documents from a vector database. Please provide variations of the query: {question} to retrieve relevant documents from a vector database. By generating multiple perspectives on the user question, your goal is to help the user overcome some of the limitations of the distance-based similarity search. Also, you need to stick to the context only. If there any other query outside the document just answer politely to the user to ask questions relevant to insurance policy.", input_variables=["question"])
    llm_chain = LLMChain(llm=llm, prompt=QUERY_PROMPT)
    retriever = MultiQueryRetriever.from_llm(vectorstore.as_retriever(), llm, prompt=QUERY_PROMPT)
    conversation_chain = ConversationalRetrievalChain.from_llm(llm=llm, retriever=retriever, memory=memory)
    return conversation_chain

def handle_userinput(conversation_chain, user_question, citation):
    response = conversation_chain({"question": user_question})
    response["citation"] = citation
    return response

# Streamlit app setup
st.title("RAG-Powered Chatbot")

# Sidebar description
st.sidebar.title("Auto Insurance Chatbot")
st.sidebar.markdown("""
Welcome!!

**How to Use**

- Simply type your question in the input box.
- For example, you can ask about what is covered in case of theft, or how to make a claim.

**Privacy**

Your interactions with the chatbot are confidential. We use your data solely to improve the service and provide accurate responses.

**Support and Feedback**

If you encounter any issues or have suggestions, please contact our support team. 

**Updates**

Stay tuned for new features and improvements.

""")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("How can I help?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Specify the path to your PDF file
    pdf_paths = ["Doc/policy-booklet-0923.pdf"]

    # Extract text from the PDF and add metadata
    text_chunks_with_metadata = []
    for pdf_path in pdf_paths:
        raw_text = get_pdf_text([pdf_path])
        text_chunks_with_metadata.extend(get_text_chunks_with_metadata(raw_text, pdf_path))

    # Create a vector store from the text chunks with metadata
    vectorstore = get_vectorstore(text_chunks_with_metadata)

    # Load additional dataset
    dataset_path = "TrainingSet_10.csv"
    df = pd.read_csv(dataset_path)

    # Prepare additional dataset text chunks with metadata
    additional_text_chunks_with_metadata = []
    for index, row in df.iterrows():
        question_excerpt_answer = f"Question: {row['Question']} Excerpt: {row['Excerpt']} Answer: {row['Answer']}"
        additional_text_chunks_with_metadata.extend(get_text_chunks_with_metadata(question_excerpt_answer, "dataset"))

    # Combine text chunks from PDF and additional dataset
    all_text_chunks_with_metadata = text_chunks_with_metadata + additional_text_chunks_with_metadata

    # Create a new vector store with combined text chunks with metadata
    vectorstore = get_vectorstore(all_text_chunks_with_metadata)

    # Create a new conversation chain with the updated vector store
    conversation_chain = get_conversation_chain(vectorstore)

    # Handle user input and get a response
    citation = "Source: Policy document and additional dataset"
    response = handle_userinput(conversation_chain, prompt, citation)

    # Display assistant response in chat message container
    bot_response = "\n".join([message.content for message in response["chat_history"] if isinstance(message, AIMessage)])
    with st.chat_message("assistant"):
        st.markdown(bot_response)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": bot_response})

    # Add feedback section
    feedback = streamlit_feedback(feedback_type="thumbs")
    st.session_state.messages[-1]["feedback"] = feedback

    # Print the citation
    st.text(response["citation"])
