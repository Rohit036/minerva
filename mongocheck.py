# streamlit_app.py

import streamlit as st
import pymongo
from pymongo.mongo_client import MongoClient

st.write("Hello")
uri = st.secrets["uri"]

# Create a new client and connect to the server
client = MongoClient(uri)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
    db = client.neuraldb
    people = db.people
    people.insert_one({"name" : "Mike", "age" : 30}) 
    people.insert_one({"name" : "Lisa", "age" : 20, "interestes" : ["C++", "Python"]}) 

    for person in people.find():
        print(person)
except Exception as e:
    print(e)
