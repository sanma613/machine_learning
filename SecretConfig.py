# You must create your own .env file with your own connection string.

from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

class SecretConfig:
    DB_URL = os.getenv("DB_URL")

    # Raise an error if DB_URL is not set in the .env file
    if not DB_URL:
        raise ValueError("DB_URL is not set. Please check your .env file.")
