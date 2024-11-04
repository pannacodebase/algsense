import time
import requests
from config import ARIA_API_KEY  # Import your API key from config.py

def query_video_status(token, request_id):
    """
    Queries the status of a video processing task.
    
    Parameters:
    - token (str): The API token for authorization.
    - request_id (str): The request ID of the video processing task.

    Returns:
    - dict: JSON response from the API or error message.
    """
    url = "https://api.rhymes.ai/v1/videoQuery"
    headers = {
        "Authorization": f"Bearer {token}",
    }
    params = {
        "requestId": request_id
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"An error occurred: {str(e)}"}

def poll_video_task(request_id, interval=10):
    """
    Polls the status of a video processing task until it's complete.

    Parameters:
    - request_id (str): The request ID of the video processing task.
    - interval (int): The time (in seconds) between each poll.

    Prints the status on each poll and stops when the task is complete.
    """
    print("Starting to poll video task status...")

    while True:
        response_data = query_video_status(ARIA_API_KEY, request_id)
        
        # Print the response for debugging
        print("Current status response:", response_data)

        # Check for the 'status' in the response
        if isinstance(response_data, dict):
            status = response_data.get('status')
            print(f"Status: {status}")

            # If the task is complete or failed, handle accordingly
            if status:
                if status.lower() == "completed":
                    # Extract video URL from the response
                    video_url = response_data.get('data')  # Assuming 'data' contains the video URL
                    print(f"Polling complete. Video URL: {video_url}")
                    break
                elif status.lower() == "failed":
                    print("Polling complete. The task has failed.")
                    break
            else:
                print("Status not found in response.")
        else:
            print("Unexpected response format:", response_data)
            break
        
        # Wait for the specified interval before polling again
        time.sleep(interval)

# Get request ID from the user
request_id = input("Please enter the request ID for the video processing task: ")
poll_video_task(request_id)
