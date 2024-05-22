
from pymongo.mongo_client import MongoClient

uri = "mongodb+srv://rohitkrsingh:<password>@minerva.85la3cg.mongodb.net/?retryWrites=true&w=majority&appName=minerva"

# Create a new client and connect to the server
client = MongoClient(uri)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    st.write("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
