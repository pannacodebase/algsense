import requests
from config import IMGBB_API_KEY  # Import the API key from config.py

def upload_image_to_imgbb(api_key, image_path):
    with open(image_path, 'rb') as image_file:
        files = {
            'image': image_file
        }
        response = requests.post(f'https://api.imgbb.com/1/upload?key={api_key}', files=files)
        
        if response.status_code == 200:
            data = response.json().get('data', {})
            print("Upload successful!")
            return {
                'id': data.get('id'),
                'title': data.get('title'),
                'url_viewer': data.get('url_viewer'),
                'url': data.get('url'),  # Direct URL
                'display_url': data.get('display_url'),
                'width': data.get('width'),
                'height': data.get('height'),
                'size': data.get('size'),
                'delete_url': data.get('delete_url'),
            }
        else:
            print("Upload failed!")
            print("Response:", response.json())
            return None  # Return None if the upload failed

if __name__ == "__main__":
    image_path = 'algae1.jpeg'  # Your image path
    upload_image_to_imgbb(IMGBB_API_KEY, image_path)  # Use the imported API key
