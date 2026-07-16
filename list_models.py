import os
from google import genai
from dotenv import load_dotenv

def list_available_models():
    # Make sure GEMINI_API_KEY is in your .env file
    load_dotenv()
    client = genai.Client()
    
    print("Available Models:")
    print("-" * 20)
    
    # Iterate through available models
    for model in client.models.list():
        # Print all available models
        print(f"- {model.name}")
            
if __name__ == "__main__":
    list_available_models()
