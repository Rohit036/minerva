import streamlit as st
from pymongo.mongo_client import MongoClient

uri = "mongodb+srv://rohitkrsingh:<password>@minerva.85la3cg.mongodb.net/?retryWrites=true&w=majority&appName=minerva"

# Create a new client and connect to the server
client = MongoClient(uri)
print(client)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Reached Here")
    st.write("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    st.write(e)
    print(e)
