import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

uri = os.getenv("MONGODB_URI")
database_name = os.getenv("DATABASE_NAME")

client = MongoClient(uri)

db = client[database_name]
profiles = db["profiles"]

profile = {
    "user_id": "U1001",
    "usual_amount_avg": 2500,
    "usual_amount_max": 5000,
    "usual_transaction_hour_start": 8,
    "usual_transaction_hour_end": 22,
    "known_beneficiaries": [
        "B101",
        "B102",
        "B103"
    ],
    "known_devices": [
        "DEV-OLD-01"
    ]
}

result = profiles.update_one(
    {"user_id": "U1001"},
    {"$set": profile},
    upsert=True
)

print("Profile inserted/updated successfully.")
print("Matched:", result.matched_count)
print("Modified:", result.modified_count)
print("Upserted:", result.upserted_id)

client.close()