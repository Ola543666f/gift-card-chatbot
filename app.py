from flask import Flask, request, jsonify, render_template, session
from functools import wraps
from config import Config
from auth import Auth
from chatbot import Chatbot

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = Config.SECRET_KEY

# Initialize components
auth = Auth()
chatbot = Chatbot()

def login_required(f):
    """Decorator to require login for routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user'):
            return jsonify({'error': 'Please login first'}), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

# ============ AUTHENTICATION ROUTES ============

@app.route('/api/signup', methods=['POST'])
def signup():
    """User signup with gift card verification"""
    data = request.json
    username = data.get('username')
    password = data.get('password')
    gift_card_code = data.get('gift_card_code')
    
    if not all([username, password, gift_card_code]):
        return jsonify({'success': False, 'message': 'All fields are required'}), 400
    
    result = auth.signup(username, password, gift_card_code)
    if result['success']:
        return jsonify(result), 201
    else:
        return jsonify(result), 400

@app.route('/api/login', methods=['POST'])
def login():
    """User login"""
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'success': False, 'message': 'Username and password required'}), 400
    
    result = auth.login(username, password)
    if result['success']:
        session['user'] = username
        session['gift_card_code'] = result['gift_card_code']
        session['verified'] = True
        return jsonify({'success': True, 'message': 'Login successful'})
    else:
        return jsonify(result), 401

@app.route('/api/verify-gift-card', methods=['POST'])
def verify_gift_card():
    """Simple gift card verification without login"""
    data = request.json
    code = data.get('code')
    
    if not code:
        return jsonify({'success': False, 'message': 'Code required'}), 400
    
    result = auth.verify_gift_card_only(code)
    if result['success']:
        session['temp_verified'] = True
        return jsonify(result)
    else:
        return jsonify(result), 401

@app.route('/api/logout', methods=['POST'])
def logout():
    """Logout user"""
    session.clear()
    return jsonify({'success': True, 'message': 'Logged out successfully'})

@app.route('/api/session', methods=['GET'])
def get_session():
    """Get current session info"""
    return jsonify({
        'authenticated': 'user' in session,
        'username': session.get('user'),
        'verified': session.get('verified', False)
    })

# ============ CHATBOT ROUTES ============

@app.route('/api/chat', methods=['POST'])
@login_required
def chat():
    """Handle chat messages (requires login)"""
    data = request.json
    user_message = data.get('message')
    
    if not user_message:
        return jsonify({'error': 'Message required'}), 400
    
    # Check verification status
    is_verified = session.get('verified', False)
    
    # Get chatbot response
    response = chatbot.get_response(user_message, is_verified)
    
    return jsonify({'response': response})

@app.route('/api/chat/temp', methods=['POST'])
def chat_temp():
    """Handle chat messages with temporary gift card verification"""
    data = request.json
    user_message = data.get('message')
    
    if not user_message:
        return jsonify({'error': 'Message required'}), 400
    
    # Check temporary verification
    is_verified = session.get('temp_verified', False)
    
    if not is_verified:
        return jsonify({'error': 'Please verify a gift card code first'}), 401
    
    # Get chatbot response
    response = chatbot.get_response(user_message, is_verified)
    
    return jsonify({'response': response})

if __name__ == '__main__':
    print("Starting Flask Server...")
    print("Open http://127.0.0.1:5000 in your browser")
    app.run(debug=True)