import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from textblob import TextBlob
import random
import warnings
warnings.filterwarnings('ignore')

class MentalHealthBot:
    def __init__(self):
        print("Initializing bot...")
        try:
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            self.load_intents()
            self.conversation_history = []
            self.current_emotion = None
            self.crisis_mode = False
            print("Bot initialized successfully!")
        except Exception as e:
            print(f"Error during initialization: {str(e)}")
            raise
        
    def load_intents(self):
        try:
            print("Loading intents...")
            with open('intents.json', 'r') as file:
                self.intents = json.load(file)['intents']
            # Create embeddings for all patterns
            self.pattern_embeddings = {}
            for intent in self.intents:
                self.pattern_embeddings[intent['tag']] = self.model.encode(intent['patterns'])
            print(f"Loaded {len(self.intents)} intents successfully!")
        except Exception as e:
            print(f"Error loading intents: {str(e)}")
            raise

    def detect_emotion(self, text):
        analysis = TextBlob(text)
        # Enhanced emotion detection
        if analysis.sentiment.polarity <= -0.5:
            return "severe_distress"
        elif analysis.sentiment.polarity < 0:
            return "mild_distress"
        elif analysis.sentiment.polarity > 0.5:
            return "positive"
        return "neutral"

    def detect_crisis(self, text):
        crisis_keywords = ['suicide', 'kill', 'die', 'end my life', 'harmful', 'hurt myself']
        return any(word in text.lower() for word in crisis_keywords)

    def find_best_intent(self, user_input):
        input_embedding = self.model.encode([user_input])[0]
        best_score = -1
        best_intent = None

        for intent in self.intents:
            for pattern_embedding in self.pattern_embeddings[intent['tag']]:
                similarity = cosine_similarity([input_embedding], [pattern_embedding])[0][0]
                if similarity > best_score:
                    best_score = similarity
                    best_intent = intent

        return best_intent if best_score > 0.3 else None

    def generate_response(self, user_input):
        # Check for crisis first
        if self.detect_crisis(user_input):
            self.crisis_mode = True
            return self.get_crisis_response()

        # Detect emotion
        current_emotion = self.detect_emotion(user_input)
        
        # Find matching intent
        matched_intent = self.find_best_intent(user_input)
        
        if matched_intent:
            response = random.choice(matched_intent['responses'])
        else:
            response = self.get_default_response(current_emotion)

        # Add emotional context
        if current_emotion == "severe_distress":
            response = f"I can hear that you're going through a really difficult time. {response}"
        elif current_emotion == "mild_distress":
            response = f"I understand this is challenging. {response}"

        # Update conversation history
        self.conversation_history.append({
            'user_input': user_input,
            'response': response,
            'emotion': current_emotion,
            'intent': matched_intent['tag'] if matched_intent else None
        })

        return response

    def get_crisis_response(self):
        return """I'm very concerned about what you're sharing. Your life matters and help is available:

1. National Crisis Hotline (24/7): 988
2. Crisis Text Line: Text HOME to 741741
3. Emergency Services: 911

Would you like to talk about what's bringing up these thoughts? I'm here to listen without judgment."""

    def get_default_response(self, emotion):
        empathetic_responses = {
            "severe_distress": [
                "I hear how difficult this is for you. Would you like to tell me more about what's troubling you?",
                "You're showing great courage in sharing this. Can you help me understand what you're going through?"
            ],
            "mild_distress": [
                "That sounds challenging. Would you like to explore these feelings together?",
                "I'm here to listen and support you. What would be most helpful right now?"
            ],
            "neutral": [
                "I'm here to listen. Would you like to tell me more?",
                "Could you share more about what's on your mind?"
            ],
            "positive": [
                "I'm glad you're sharing this with me. Would you like to tell me more?",
                "Thank you for sharing. What else is on your mind?"
            ]
        }
        return random.choice(empathetic_responses[emotion])

    def process_input(self, user_input):
        try:
            return self.generate_response(user_input)
        except Exception as e:
            print(f"Error processing input: {str(e)}")
            return "I apologize, but I'm having trouble understanding. Could you rephrase that?"

    def start_chat(self):
        """Start the chat interaction"""
        print("\nMental Health Bot: Hi, I'm here to support you. How are you feeling today?")
        print("(Type 'exit' to end our conversation)")
        
        while True:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() == 'exit':
                print("\nMental Health Bot: Take care! Remember, it's okay to reach out for help when you need it.")
                break
            
            try:
                response = self.process_input(user_input)
                print("\nMental Health Bot:", response)
            except Exception as e:
                print("\nMental Health Bot: I apologize, but I'm having trouble processing that. Could you try rephrasing?")

def main():
    try:
        bot = MentalHealthBot()
        bot.start_chat()
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print("Please ensure all required packages are installed and the dataset file is present.")

if __name__ == "__main__":
    main()