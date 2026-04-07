import hashlib
import secrets
from database import Database

class Auth:
    def __init__(self):
        self.users_data = Database.load_users()
        self.gift_cards = Database.load_gift_cards()
        self.hashed_gift_cards = Database.hash_gift_codes(self.gift_cards)
    
    def hash_password(self, password, salt=None):
        """Hash password with salt using SHA-256"""
        if salt is None:
            salt = secrets.token_hex(16)  # Generate random salt
        
        # Combine password and salt, then hash
        salted_password = password + salt
        hashed = hashlib.sha256(salted_password.encode()).hexdigest()
        
        return hashed, salt
    
    def verify_password(self, password, salt, stored_hash):
        """Verify password against stored hash"""
        hashed, _ = self.hash_password(password, salt)
        return hashed == stored_hash
    
    def signup(self, username, password, gift_card_code):
        """Register a new user with gift card verification"""
        # Check if username already exists
        for user in self.users_data['users']:
            if user['username'] == username:
                return {'success': False, 'message': 'Username already exists'}
        
        # Verify gift card code
        gift_card_code = gift_card_code.strip().upper()
        if gift_card_code not in self.gift_cards:
            return {'success': False, 'message': 'Invalid gift card code'}
        
        # Hash password with salt
        hashed_password, salt = self.hash_password(password)
        
        # Create new user
        new_user = {
            'username': username,
            'password_hash': hashed_password,
            'salt': salt,
            'gift_card_code': gift_card_code,  # Store the actual code 
            'created_at': None  
        }
        
        self.users_data['users'].append(new_user)
        Database.save_users(self.users_data)
        
        return {'success': True, 'message': 'Signup successful'}
    
    def login(self, username, password):
        """Login user with username and password"""
        for user in self.users_data['users']:
            if user['username'] == username:
                if self.verify_password(password, user['salt'], user['password_hash']):
                    return {
                        'success': True, 
                        'message': 'Login successful',
                        'gift_card_code': user['gift_card_code']
                    }
                else:
                    return {'success': False, 'message': 'Invalid password'}
        
        return {'success': False, 'message': 'Username not found'}
    
    def verify_gift_card_only(self, code):
        """Verify gift card code without login (for simple verification)"""
        code = code.strip().upper()
        if code in self.gift_cards:
            return {'success': True, 'message': 'Valid gift card code'}
        return {'success': False, 'message': 'Invalid gift card code'}