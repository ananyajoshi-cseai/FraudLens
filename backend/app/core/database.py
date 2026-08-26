from pymongo import MongoClient
from app.core.config import MONGODB_URI, DATABASE_NAME

# Global variables to hold the database connection
client = None
db = None

def connect_db():
    global client, db
    print("Connecting to MongoDB Atlas...")
    client = MongoClient(MONGODB_URI)
    db = client[DATABASE_NAME]
    # Ping to verify
    client.admin.command('ping')
    print("Successfully connected to MongoDB!")

def close_db():
    global client
    if client:
        client.close()
        print("MongoDB connection closed.")

def get_db():
    """Dependency injection function for FastAPI routes"""
    return db