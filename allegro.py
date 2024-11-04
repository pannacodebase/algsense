import requests
import time
from config import ALLEGRO_API_KEY

# Function to generate video based on specific use cases
def generate_video(refined_prompt):
    url = "https://api.rhymes.ai/v1/generateVideoSyn"
    headers = {
        "Authorization": f"Bearer {ALLEGRO_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "refined_prompt": refined_prompt,
        "num_step": 100,
        "cfg_scale": 7.5,
        "user_prompt": refined_prompt,
        "rand_seed": 12345,
        "user_id": "3",
        "original_prompt": refined_prompt
    }

    response = requests.post(url, headers=headers, json=data)
    response_data = response.json()

    if response_data.get("status") == 0:
        request_id = response_data.get("data")
        print("Video generation started. Request ID:", request_id)
        # Wait for the video to be processed and get the link
        video_url = poll_video_task(request_id)
        return video_url
    else:
        print("Failed to start video generation:", response_data.get("message"))
        return None

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

def poll_video_task(request_id, interval=120):
    """
    Polls the status of a video processing task until it's complete.

    Parameters:
    - request_id (str): The request ID of the video processing task.
    - interval (int): The time (in seconds) between each poll.

    Returns:
    - str: The video URL if the task is completed.
    """
    print("Starting to poll video task status...")

    while True:
        response_data = query_video_status(ALLEGRO_API_KEY, request_id)
        
        # Print the response for debugging
        print("Current status response:", response_data)

        # Check for the 'status' in the response
        if isinstance(response_data, dict):
            status = response_data.get('status')
            # Check if the task is completed
            if status == 0:  # Assuming status 0 means success
                video_url = response_data.get('data')
                if video_url:
                    print(f"Polling complete. Video URL: {video_url}")
                    return video_url  # Return the video URL
                else:
                    print("Video is still processing. Waiting...")
            else:
                print("Polling complete. The task has failed.")
                break
        
        # Wait for the specified interval before polling again
        time.sleep(interval)

# Example Usage
# Uncomment the following lines if you want to test directly from this file.
# use_case = "your_refined_prompt_here"
# video_link = generate_video(use_case)
# print(f"Generated video link: {video_link}")
