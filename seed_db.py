import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

# Connect to Atlas
client = MongoClient(os.getenv("MONGODB_URI"))
db = client[os.getenv("DATABASE_NAME")]
collection = db["profiles"]

# Clean up any previous test runs
collection.delete_many({"user_id": "test_user_01"})

# Insert our dummy profile
dummy_profile = {
    "user_id": "test_user_01",
    "usual_amount_avg": 1200.0,
    "usual_amount_max": 5000.0,
    "usual_transaction_hour_start": 8,
    "usual_transaction_hour_end": 22,
    "known_beneficiaries": ["B101", "B205", "B310"],
    "known_devices": ["DEV-OLD-01"]
}

result = collection.insert_one(dummy_profile)
print(f"Success! Inserted dummy profile for 'test_user_01' into MongoDB.")