from datetime import datetime

import os
from pymongo import MongoClient
# from dotenv import load_dotenv


# load_dotenv()

import streamlit as st

# mongo_uri = os.getenv("MONGO_URI")
# mongo_uri = os.getenv("uri")
# db_name = os.getenv("DB_NAME")

mongo_uri = st.secrets["uri"]
db_name = st.secrets("DB_NAME")

client = MongoClient(mongo_uri)
db = client[db_name]

conversations_collection = db.conversations

def save_message(session_id, message_type, content):
    message_document = {
        "session_id": session_id,
        "type": message_type,
        "content": content,
        "timestamp": datetime.utcnow()
    }
    conversations_collection.insert_one(message_document)


def get_chat_history_by_session_id(session_id):
    # Retrieve all documents that match the session_id
    messages = list(conversations_collection.find({"session_id": session_id}).sort("timestamp", 1))
    return messages

def get_all_session_ids():
    # Retrieve all unique session IDs from the database
    sessions = conversations_collection.distinct("session_id")
    return sessions
