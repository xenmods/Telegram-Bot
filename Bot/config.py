import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN", "")
    API_ID = int(os.getenv("API_ID", "6"))
    API_HASH = os.getenv("API_HASH", "eb06d4abfb49dc3eeb1aeb98ae0f581e")
    DB_URI = os.getenv("DB_URI", "sqlite+aiosqlite:///Bot.db")
    MONGO_URI = os.getenv("MONGO_URI", os.getenv("MONGO_URL", ""))
    DB_NAME = os.getenv("DB_NAME", "sample")

