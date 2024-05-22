import streamlit as st
import os
import json
from datetime import datetime
from pymongo import MongoClient
from langchain_core.messages import AIMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from utils import save_message, get_all_session_ids, get_chat_history_by_session_id

import uuid

with open('config.json', 'r') as f:
    config = json.load(f)

# Define get_response function (assuming it's not defined elsewhere in the given code)
def get_response(user_query, chat_history):
    # template = os.getenv("CHAT_TEMPLATE", "Default prompt if not set in .env file")
    template = config["CHAT_TEMPLATE"]
    prompt = ChatPromptTemplate.from_template(template)
    llm = ChatOpenAI()
    chain = prompt | llm | StrOutputParser()
    return chain.stream({
        "chat_history": chat_history,
        "user_question": user_query,
    })

# Function to reset or initialize session state for new run
def initialize_new_run():
    st.session_state.session_id = str(uuid.uuid4())  # Generate a new session ID
    st.session_state.chat_history = []  # Reset chat history

# app config
st.set_page_config(page_title="AutoInsure Assistant", page_icon="🤖")
st.title("AutoInsure Assistant")
st.subheader("Your go-to virtual assistant for quick car insurance quotes")

# Initialize session state if not already set
if 'session_id' not in st.session_state or 'chat_history' not in st.session_state:
    initialize_new_run()

# Display the current session ID in the sidebar
st.sidebar.write(f"**Current Session ID:** `{st.session_state.session_id}`")

# Sidebar buttons for navigation
if st.sidebar.button("Get New Quotation"):
    st.session_state.current_view = 'chat'
    initialize_new_run()
    st.rerun()     
elif st.sidebar.button("Historical Data"):
    st.session_state.current_view = 'data'

# Conditional display based on current view
if 'current_view' not in st.session_state or st.session_state.current_view == 'chat':
    multi = '''Hello there! Welcome to our registration office in the car insurance company. \n 
    How can I help you today? Do you have a specific type of car in mind that you
    would like to get quote for? \n 
    Please let me know the make and model, as well as the year of manufacturing and license plate number. \n 
    Once I have this information, I will be able to provide you with an accurate annual cost of insurance. 
    And by the way may I have your name please?
    '''
    st.markdown(multi)

    # Display chat history
    for message in st.session_state.chat_history:
        if isinstance(message, AIMessage):
            with st.chat_message("AI"):
                st.write(message.content)
        elif isinstance(message, HumanMessage):
            with st.chat_message("Human"):
                st.write(message.content)

    # User input
    user_query = st.chat_input("Type your message here...")
    if user_query is not None and user_query != "":
        st.session_state.chat_history.append(HumanMessage(content=user_query))

        save_message(st.session_state.session_id, "Human", user_query)

        with st.chat_message("Human"):
            st.markdown(user_query)

        with st.chat_message("AI"):
            response = st.write_stream(get_response(user_query, st.session_state.chat_history))
            save_message(st.session_state.session_id, "AI", response)

        st.session_state.chat_history.append(AIMessage(content=response))

elif st.session_state.current_view == 'data':
    st.write("Historical Data Overview")
    session_ids = get_all_session_ids()
    selected_session_id = st.selectbox("Select a session to view history:", session_ids)

    if st.button("Fetch Session History"):
        session_history = get_chat_history_by_session_id(selected_session_id)
        for message in session_history:
            st.write(f"{message['timestamp'].strftime('%Y-%m-%d %H:%M:%S')} - {message['type']} - {message['content']}")
