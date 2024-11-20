from flask import Flask, request, jsonify
from flask_cors import CORS
from chatbot import MentalHealthBot
import traceback
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:5173"],
        "methods": ["OPTIONS", "GET", "POST"],
        "allow_headers": ["Content-Type"]
    }
})

try:
    print("Initializing chatbot...")
    chatbot = MentalHealthBot()
except Exception as e:
    print(f"Error initializing chatbot: {str(e)}")
    traceback.print_exc()
    exit(1)

@app.route('/api/chat', methods=['POST', 'OPTIONS'])
def chat():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
        
    try:
        data = request.json
        user_input = data.get('message', '')
        
        if not user_input:
            return jsonify({'error': 'No message provided'}), 400
            
        response = chatbot.process_input(user_input)
        return jsonify({'response': response})
        
    except Exception as e:
        print(f"Error processing message: {str(e)}")
        traceback.print_exc()
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))
    host = os.getenv('HOST', '0.0.0.0')
    app.run(debug=True, port=port, host=host)