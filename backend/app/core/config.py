import os
from dotenv import load_dotenv

# Load variables from the .env file in the root directory
load_dotenv()

# MongoDB Configuration
MONGODB_URI = os.getenv("MONGODB_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME", "fraudlens")

# Risk Engine Constants
LOW_RISK_MAX = 30
MEDIUM_RISK_MAX = 60
MAX_RISK_SCORE = 100