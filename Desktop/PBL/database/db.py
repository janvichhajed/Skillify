from pymongo import MongoClient

# connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")

# database name
db = client["skillify"]

# collections
users = db["users"]
skills = db["skills"]
sessions = db["sessions"]
certificates = db["certificates"]
feedback = db["feedback"]
proofs = db["proofs"]