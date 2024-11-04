import requests
import json
from config import SERPER_API_KEY  # Import API key securely
from aria import ask_aria  # Import the ask_aria function from aria.py
from flask import Flask, render_template, jsonify

app = Flask(__name__)

def fetch_news(query):
    url = 'https://google.serper.dev/news'
    headers = {
        'X-API-KEY': SERPER_API_KEY,
        'Content-Type': 'application/json'
    }
    data = {
        'q': query
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        return response.json()  # Return the JSON response
    else:
        print(f"Error fetching news: {response.status_code} - {response.text}")
        return None

def process_news(news_data):
    messages = []
    if "news" in news_data:
        for item in news_data["news"]:
            title = item.get("title")
            snippet = item.get("snippet")
            message = f"Title: \nSnippet: {snippet}\n"
            messages.append(message)
    
    return "\n".join(messages)  # Return the combined messages


if __name__ == '__main__':
    app.run(debug=True)
