from datetime import datetime

import os
from pymongo import MongoClient
import json
from dotenv import load_dotenv
import streamlit as st


# Load the configuration file
with open('config.json', 'r') as f:
    config = json.load(f)
    dev = config["development"]

if dev == True:
    load_dotenv()    
    try:
        client = MongoClient(os.getenv("ATLAS_URI"))
        db = client[os.getenv("DB_NAME")]  # Ensure you have 'mongo_uri' and 'db_name' in your config
    except Exception as e:
        st.error(f"Failed to connect to the database: {str(e)}")
        raise SystemExit("Exiting: Database connection failed.")
else:
    try:
        client = MongoClient(st.secrets["ATLAS_URI"])
        db = client[st.secrets["DB_NAME"]]
    except Exception as e:
        st.error(f"Failed to connect to the database: {str(e)}")
        raise SystemExit("Exiting: Database connection failed.")

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
