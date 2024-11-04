import requests
from config import ARIA_API_KEY  # Import API key securely

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
