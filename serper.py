import requests
import wikipedia
from config import SERPER_API_KEY

# Set the language to English for Wikipedia
wikipedia.set_lang("en")

# Function to perform a search using the Google Serper API
def google_serper_search(query):
    # Append " algae formations" to the query
    query += " algae formations"
    
    url = 'https://google.serper.dev/search'
    headers = {
        'X-API-KEY': SERPER_API_KEY,
        'Content-Type': 'application/json'
    }
    data = {
        'q': query
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()  # Return the JSON response
    else:
        return f"Error: {response.status_code}, {response.text}"

# Function to format the Google Serper results
def format_google_results(results):
    formatted_results = []
    
    for result in results.get('organic', []):
        title = result.get('title', '')
        link = result.get('link', '')
        snippet = result.get('snippet', '')
        formatted_results.append(f"{title} {link} {snippet}")

    return " ".join(formatted_results)

# Function to get a summary from Wikipedia
def get_wikipedia_summary(query):
    # Use the original query without appending
    try:
        summary = wikipedia.summary(query)
        return summary
    except Exception as e:
        return str(e)

# Example usage
if __name__ == "__main__":
    # Define the search query
    search_query = "vistula river"  # Pass your search term here

    # Perform a Google Serper API search
    google_results = google_serper_search(search_query)

    # Initialize a variable to hold the combined results
    combined_results = ""

    # Check if results are valid before formatting
    if isinstance(google_results, dict):
        formatted_results = format_google_results(google_results)
        combined_results += f"Google Serper Results: {formatted_results} "

    # Get a Wikipedia summary
    summary = get_wikipedia_summary(search_query)
    combined_results += f"Wikipedia Summary: {summary}"

    # Remove any excess whitespace
    combined_results = " ".join(combined_results.split())

    # Print the final combined result
    print(combined_results)
