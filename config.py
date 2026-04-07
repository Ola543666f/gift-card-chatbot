import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
    SECRET_KEY = os.environ.get("SECRET_KEY", os.urandom(24))
    DEBUG = True
    DATA_DIR = "data"
    GIFT_CARDS_FILE = "data/gift_cards.json"
    USERS_FILE = "data/users.json"
    FAQ_FILE = "data/faq.txt"