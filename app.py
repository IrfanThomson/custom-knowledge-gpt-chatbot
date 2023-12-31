import os
import openai
import streamlit as st
from dotenv import load_dotenv
from render import bot_msg_container_html_template, user_msg_container_html_template
from utils import semantic_search
from langchain.vectorstores import Chroma, Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
import prompts
import pinecone


# Set up OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]
pinecone.init(api_key=st.secrets["PINECONE_API_KEY"], environment=st.secrets["PINECONE_ENVIRONMENT"])
embeddings = OpenAIEmbeddings()
docsearch = Pinecone.from_existing_index(index_name=st.secrets["PINECONE_INDEX_NAME"], embedding=embeddings)

st.header("Dr K GPT - By Irfan Thomson")

# Define chat history storage
if "history" not in st.session_state:
    st.session_state.history = []

# Construct messages from chat history
def construct_messages(history):
    messages = [{"role": "system", "content": prompts.system_message}]
    
    for entry in history:
        role = "user" if entry["is_user"] else "assistant"
        messages.append({"role": role, "content": entry["message"]})
    
    return messages

# Generate response to user prompt
def generate_response():
    st.session_state.history.append({
        "message": st.session_state.prompt,
        "is_user": True
    })
    query = st.session_state.prompt
    print(f"Query: {query}")

    # Perform semantic search and format results
    search_results = docsearch.similarity_search(query)
    context = ""
    for doc in search_results:
        context += doc.page_content[:2000]

    # Generate human prompt template and convert to API message format
    query_with_context = prompts.human_template.format(query=query, context=context)

    # Convert chat history to a list of messages
    messages = construct_messages(st.session_state.history)
    messages.append({"role": "user", "content": query_with_context})

    # Run the LLMChain
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    print(messages)

    # Parse response
    bot_response = response["choices"][0]["message"]["content"]
    st.session_state.history.append({
        "message": bot_response,
        "is_user": False
    })

# User input prompt
user_prompt = st.text_input("Enter your prompt:",
                            key="prompt",
                            placeholder="e.g. 'How do I find motivation and become more productive?'",
                            on_change=generate_response
                            )

# Display chat history
for message in st.session_state.history:
    if message["is_user"]:
        st.write(user_msg_container_html_template.replace("$MSG", message["message"]), unsafe_allow_html=True)
    else:
        st.write(bot_msg_container_html_template.replace("$MSG", message["message"]), unsafe_allow_html=True)
