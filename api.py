import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if GEMINI_API_KEY is None:
    print("ERROR: Could not find GEMINI_API_KEY in environment variables!")
    print("Please check your .env file")
    exit(1)

genai.configure(api_key=GEMINI_API_KEY)

def get_gemini_response(system_prompt, user_message):
    """Get response from Gemini API with system prompt"""
    try:
        
        model = genai.GenerativeModel('models/gemini-2.5-flash')
        
        
        # Combine prompts
        full_prompt = f"{system_prompt}\n\nUser: {user_message}\nAssistant:"
        
        # Generate response
        response = model.generate_content(full_prompt)
        
        return response.text
        
    except Exception as e:
        print(f"Gemini API Error Details: {e}")
        return f"I apologize, but I'm having trouble processing your request. (Error: {str(e)})"