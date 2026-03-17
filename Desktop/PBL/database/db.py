from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

db = client["skillify"]

users = db["users"]
skills = db["skills"]
sessions = db["sessions"]
certificates = db["certificates"]
feedback = db["feedback"]
proofs = db["proofs"]