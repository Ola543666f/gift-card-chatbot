import json
import hashlib
import os
from config import Config

class Database:
    @staticmethod
    def load_gift_cards():
        """Load gift card codes from JSON"""
        try:
            with open(Config.GIFT_CARDS_FILE, 'r') as f:
                data = json.load(f)
                return data['valid_codes']
        except FileNotFoundError:
            # Create default file if it doesn't exist
            os.makedirs(Config.DATA_DIR, exist_ok=True)
            default_data = {"valid_codes": ["GIFT24", "SAVE10", "PROMO5", "HAPPY7", "REDEEM", "OFF100"]}
            with open(Config.GIFT_CARDS_FILE, 'w') as f:
                json.dump(default_data, f, indent=2)
            return default_data['valid_codes']
    
    @staticmethod
    def hash_gift_codes(codes):
        """Hash gift card codes for secure storage"""
        return [hashlib.sha256(code.encode()).hexdigest() for code in codes]
    
    @staticmethod
    def load_faqs():
        """Load FAQs from text file"""
        try:
            with open(Config.FAQ_FILE, 'r') as f:
                return f.read()
        except FileNotFoundError:
            os.makedirs(Config.DATA_DIR, exist_ok=True)
            default_faq = "Q: How do I redeem my gift card?\nA: Enter your code in the redeem section."
            with open(Config.FAQ_FILE, 'w') as f:
                f.write(default_faq)
            return default_faq
    
    @staticmethod
    def load_users():
        """Load users from JSON file"""
        try:
            with open(Config.USERS_FILE, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            os.makedirs(Config.DATA_DIR, exist_ok=True)
            default_users = {"users": []}
            with open(Config.USERS_FILE, 'w') as f:
                json.dump(default_users, f, indent=2)
            return default_users
    
    @staticmethod
    def save_users(users_data):
        """Save users to JSON file"""
        with open(Config.USERS_FILE, 'w') as f:
            json.dump(users_data, f, indent=2)