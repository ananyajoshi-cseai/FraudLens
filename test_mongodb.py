from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

uri = os.getenv("MONGODB_URI")
database_name = os.getenv("DATABASE_NAME")

print("URI loaded:", bool(uri))
print("Database:", database_name)

try:
    client = MongoClient(uri, serverSelectionTimeoutMS=5000)

    # Test connection
    client.admin.command("ping")

    print("MongoDB connection successful!")

    db = client[database_name]

    # Test write
    collection = db["connection_test"]

    result = collection.insert_one({
        "test": True,
        "message": "FraudLens MongoDB connection test"
    })

    print("Test document inserted:", result.inserted_id)

    # Test read
    document = collection.find_one({"_id": result.inserted_id})

    print("Test document found:", document)

    print("MongoDB read/write test successful!")

    client.close()

except Exception as e:
    print("MongoDB connection FAILED")
    print(type(e).__name__, ":", e)