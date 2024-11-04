from flask import Flask, jsonify
import requests
from config import ARIA_API_KEY  # Import API key securely

app = Flask(__name__)

def ask_aria(user_message):
    """Send a user's message to Aria's API and return the response."""
    payload = {
        "model": "aria",
        "messages": [
            {
                "role": "user",
                "content": user_message  # Send the full prompt as content
            }
        ],
        "temperature": 0.6,
        "max_tokens": 1024,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0,
        "stream": False,
        "stop": ["<|im_end|>"],
    }

    try:
        response = requests.post(
            'https://api.rhymes.ai/v1/chat/completions',
            headers={
                'Authorization': f'Bearer {ARIA_API_KEY}',
                'Content-Type': 'application/json'
            },
            json=payload
        )

        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return f"Error: {response.status_code} - {response.text}"

    except Exception as e:
        return f"An error occurred: {str(e)}"

# Function to get a sample transcript on algal blooms
def get_algal_bloom_transcript():
    prompt = (
        "Please provide a conversation transcript about algal blooms in the following format. The below is a sample, create your own:\n"
        "Use these characters: aura-hera-en (Hera, girl), aura-orion-en (Orion, boy), aura-luna-en (Luna, girl), aura-orpheus-en (Orpheus, boy), and aura-arcas-en (Arcas, boy).\n\n"
        "Format of output is : { avatar: 'aura-hera-en', gender: 'girl', text: \"Hello everyone! Let's talk about algal blooms.\" },\n"
        "Ensure all keys in the JSON objects are enclosed in double quotes (e.g., change avatar to \"avatar\"). Enclose all objects in square brackets ([ ]) to create a valid JSON array. Remove any trailing comma after the last object in the collection, as the last item in an array or object must not have a trailing comma.\n"
        "Use of Apostrophes in Strings: Ensure your system can handle strings with apostrophes like \"Let’s\" and \"can’t\" correctly; you can escape them with a backslash (\\') if needed, but it's not necessary unless you encounter issues."
    )




    return ask_aria(prompt)


if __name__ == "__main__":
    app.run(debug=True)
