from pymongo import MongoClient
import urllib.parse
from config import Config

# Connect to MongoDB using connection string from Config
client = MongoClient(Config.MONGO_URI)

# Database Name
db = client["skillify"]

# Collections
users = db["users"]
proofs = db["proofs"]
skills = db["skills"]
sessions = db["sessions"]
feedback = db["feedback"]
certificates = db["certificates"]

# Indexes for fast querying
users.create_index("email", unique=True)
skills.create_index("title")
sessions.create_index("requester_id")
sessions.create_index("provider_id")
certificates.create_index("certificate_hash", unique=True)