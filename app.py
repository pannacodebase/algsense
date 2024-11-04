import base64
import requests
import os
import sqlite3
import tempfile  # Import tempfile
from flask import Flask, render_template, request, jsonify
from aria import ask_aria  # Import the correct function
from db_handler import insert_marker, update_marker_images, test_database_connection, get_all_markers  # Import the necessary functions
from serper import google_serper_search, get_wikipedia_summary, format_google_results  # Import the functions from serper.py
from aria_img import analyze_image
from imgbb import upload_image_to_imgbb
from allegro import generate_video as allegro_generate_video  # Import the function from allegro.py
from config import IMGBB_API_KEY  # Import the API key from config.py
from config import ALLEGRO_API_KEY
from news import process_news, fetch_news
from config import DEEPGRAM_API_KEY
from converse import get_algal_bloom_transcript 
import logging

app = Flask(__name__)

@app.route('/')
def index():
    # Retrieve all markers from the database when the index page is loaded
    markers = get_all_markers()
    return render_template('index.html', markers=markers)

@app.route('/home')
def home():
    # Retrieve all markers from the database when the home page is loaded
    markers = get_all_markers()
    return render_template('index.html', markers=markers)

@app.route('/simu')
def simu():
    # Retrieve all markers from the database when the home page is loaded
    markers = get_all_markers()
    return render_template('simu.html', markers=markers)

@app.route('/algal-bloom-transcript', methods=['GET'])
def algal_bloom_transcript():
    transcript = get_algal_bloom_transcript()
    return jsonify(transcript=transcript)

@app.route('/dataana')
def dataana():
    return render_template('dataana.html')

@app.route('/converse')
def converse():
    return render_template('converse.html')

@app.route('/fetch_news', methods=['GET'])
def get_news():
    query = "algal blooms"
    news_data = fetch_news(query)
    
    if news_data:
        news_message = process_news(news_data)
        pre_prompt = (
            "Summarize to 5 sentences. You are Katy, a  news reader! Start with a warm, friendly greeting, like you’re catching up over coffee with a friend. ☕️ "
            "NO EMOJI's please.Introduce the topic with a fun, relatable comment—something lighthearted to make the reader smile. Keep your tone casual, playful, and engaging. "
            "Use friendly phrases like 'aah' and 'you know' to make it feel relaxed, and sprinkle in some emojis (but not too many) to add warmth. 😄 "
            "Summarize the topic in a single, cozy paragraph, making sure its easy to understand and free of any technical language or formatting. "
            "Imagine youre chatting on a porch, soaking up the sunshine. ☀️ Let's make it feel like a fun, friendly catch-up!"
        )
        full_message = pre_prompt + news_message
        full_message = ' '.join(full_message.split()).replace('\n', ' ')
        response = ask_aria(full_message)
        return jsonify({'summary': response})
    
    return jsonify({'error': 'Failed to fetch news'}), 500


@app.route('/generate_video', methods=['POST'])
def generate_video():
    data = request.get_json()
    refined_prompt = data.get("prompt")

    if not refined_prompt:
        return jsonify({"status": "error", "message": "No prompt provided"}), 400

    # Call the generate_video function from allegro.py
    request_id = allegro_generate_video(refined_prompt)  # Process video generation in allegro.py

    if request_id:
        return jsonify({"status": "success", "request_id": request_id})
    else:
        return jsonify({"status": "error", "message": "Failed to start video generation."})


# Endpoint to check the video status
@app.route('/query_video_status', methods=['GET'])
def query_video_status():
    request_id = request.args.get("request_id")
    url = "https://api.rhymes.ai/v1/videoQuery"
    headers = {"Authorization": f"Bearer {ALLEGRO_API_KEY}"}
    params = {"requestId": request_id}

    response = requests.get(url, headers=headers, params=params)
    response_data = response.json()

    if response_data.get("status") == 0:
        video_link = response_data.get("data")
        if video_link:
            return jsonify({"status": "success", "video_link": video_link})
        else:
            return jsonify({"status": "processing"})
    else:
        return jsonify({"status": "error", "message": response_data.get("message")})


@app.route('/upload_images', methods=['POST'])
def upload_images():
    results = []
    marker_id = request.form.get('marker_id')  # Get the marker ID
    images = request.files.getlist('images')  # Get the uploaded images

    for image in images:
        try:
            # Create a temporary file to save the uploaded image
            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpeg') as temp_file:
                temp_image_path = temp_file.name  # Get the path of the temporary file
                image.save(temp_image_path)  # Save the uploaded image temporarily

            # Convert the image file to base64
            with open(temp_image_path, "rb") as img_file:
                image_base64 = base64.b64encode(img_file.read()).decode('utf-8')

            # Analyze the image
            result = analyze_image(image_base64)  # Call function in aria_img.py
            results.append(result)

            # Upload the image to imgbb and get the direct link
            upload_response = upload_image_to_imgbb(IMGBB_API_KEY, temp_image_path)
            if upload_response:
                direct_url = upload_response.get('url')  # Get the direct URL from the response
                if direct_url:
                    update_marker_images(marker_id, direct_url)  # Update marker in DB
                else:
                    raise ValueError("Failed to get the direct URL from imgbb response.")
            else:
                raise ValueError("Failed to upload image to imgbb.")

        except Exception as e:
            print(f"Error processing image: {e}")
            results.append({"error": str(e)})
        finally:
            # Delete the temporary file after processing
            if os.path.exists(temp_image_path):
                os.remove(temp_image_path)

    return jsonify(results)


@app.route('/generate_summary', methods=['POST'])
def generate_summary():
    data = request.json
    location = data.get('location')
    
    if location:
        # Perform the Google Serper search
        google_results = google_serper_search(location)
        formatted_results = format_google_results(google_results)  # Now this should work
        
        # Get the Wikipedia summary
        wiki_summary = get_wikipedia_summary(location)
        
        # Combine results and generate a custom prompt for Aria
        custom_prompt = (
            f"Summarize the provided location in one line. Wikipedia Summary: {wiki_summary}"
            f"Use the following information:   Google Results: {formatted_results}"
            f"Include details about the composition of algae blooms, challenges, risks, issues and their prevalence in 2-3 lines. "
            f"Ensure the overall text does not exceed 4 lines and is formatted as a paragraph. "
        )
       
        # Pass this prompt to Aria
        aria_response = ask_aria(custom_prompt)
        
        return jsonify({"summary": aria_response})
    else:
        return jsonify({"summary": "No location provided."})

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if user_message:
        # Process message with Aria
        response = ask_aria(user_message)
        return jsonify({"response": response})
    else:
        return jsonify({"response": "No message received."})

# New endpoint for generating a marker based on a command
@app.route('/generate_marker', methods=['POST'])
def generate_marker():
    user_message = request.json.get('message')
    if "marker" in user_message:
        # Send a custom prompt to Aria to get coordinates
        prompt = f"No Prefix or suffix. No other text. Assume the most logical location if not clear. Provide only the nearest river (with suffix river if not there) at the location, latitude, longitude coordinates for the location mentioned: '{user_message}' as river name, two numbers separated by a comma. For example: 'kovam river, 51.1055, 17.0355'"
        aria_response = ask_aria(prompt)
        print(aria_response)        
        # Assuming Aria returns a response in the format: "poland, 53.44, 33.44"
        try:
            coords = extract_coordinates_from_response(aria_response)
            location_name = coords[0]  # Use the first part as the location name
            latitude = coords[1]
            longitude = coords[2]
            print(location_name)            # Insert marker into the database
            insert_marker(location_name, latitude, longitude)
            response_message = f"Marker added at Latitude: {latitude}, Longitude: {longitude}"
            print(response_message)
            return jsonify({"coords": coords, "response": response_message})
        except ValueError:
            return jsonify({"response": "Could not parse coordinates from the response."})
    else:
        return jsonify({"response": "No marker command found in the message."})

def extract_coordinates_from_response(response):
    import re
    match = re.search(r"([^,]+),\s*(-?\d+\.\d+),\s*(-?\d+\.\d+)", response)
    if match:
        location = match.group(1).strip()  # Location name
        latitude = float(match.group(2))    # Latitude
        longitude = float(match.group(3))   # Longitude

        return [location, latitude, longitude]
    else:
        raise ValueError("Coordinates not found in response.")

@app.route('/insights', methods=['POST'])
def insights():
    data = request.get_json()  # Get the JSON data sent from the frontend
    prompt = data.get('prompt', '')
    # Define the pre_prompt with instructions and thematic elements
    pre_prompt = (
        "Your task is to analyze the below information and suggest how impacted the lake is from algae bloom perspective:\n"
        "Write it as 1 paragraph. Dont bold or use any italics. just simple text (4-6 line sentences) and lots of emojis\n"
        f"{prompt}\n"
    )
    aria_response = ask_aria(pre_prompt)
    print(aria_response)  # Now the pre_prompt includes the user's prompt directly

    # Format the aria_response into a scene description, if necessary
    # This part would depend on how you want to structure aria's response
    
    return jsonify({
        'status': 'success', 
        'message': 'Prompt received', 
        'refinedPrompt': pre_prompt, 
        'ariaResponse': aria_response
    })


@app.route('/refine', methods=['POST'])
def refine():
    data = request.get_json()  # Get the JSON data sent from the frontend
    prompt = data.get('prompt', '')
    # Define the pre_prompt with instructions and thematic elements
    pre_prompt = (
        "Your task is to create a scene based on the following conditions:\n"
        "Please present your results in this format:\n"
        "Scene 1: <description>\n"
        "Write the description as a paragraph only. Make sure to include the mandatory items (algae type, growth condition, water type) in your description. For algae type, include a detailed expansion on its appearance, properties, attributes, shape, size, and texture (4-5 lines long).\n"
        f"{prompt}\n"
        "Select specific parameters from the following categories, incorporating unique settings, angles, and camera configurations for realism:\n"
        "- Algae Type: (Specify details about its appearance, shape, size, and texture)\n"
        "- Growth Condition: (Nutrient-rich waters, warm temperatures, stagnant waters, eutrophication, seasonal temperature variations, explain how these conditions affect the algae)\n"
        "- Water Type: (Freshwater, brackish water, polluted water, saline water, turbid water, describe the water's condition and its impact on the algae)\n"
        "- Subject: [Toxic algae blooms, Dead fish, Insects infesting the area]\n"
        "- Activity: [Pollution effects, Decomposition, Insect swarming]\n"
        "- Background: [Lifeless banks, Trash-filled shores, Industrial wasteland]\n"
        "- Light: [Dull overcast light, Harsh artificial lighting, Gloomy twilight]\n"
        "- Angle: [Ground level with a grim perspective, Aerial view of pollution spread, Close-up on decay]\n"
        "- Style: [Grim realism, Distorted interpretation, Depressing depiction]\n"
        "- Artistic Medium: [Digital art focusing on decay, Dark watercolor, Oil painting with heavy strokes]\n"
        "- Color Palette: [Sickly greens and browns, Dark and murky shades, Muted, lifeless colors]\n"
        "- Exclusions: [Natural beauty, Wildlife, Clear water]\n"
        "- Aspect Ratio: [16:9, 4:3, Square]\n"
        "- Character Details: [None specified, Dead animals, Swarms of flies]\n"
        "- Props: [Debris and trash, Stagnant water, Algae-covered rocks]\n"
        "- Setting: [Contaminated river lined with refuse, An abandoned industrial site, A dead-end waterway]\n"
        "- Atmosphere: [Dreary and oppressive, Stagnant and decaying, Uninviting and dark]\n"
        "- Visual Composition: [Chaotic with a focus on pollution, Centered on decay, Distracting clutter]\n"
        "- Emotional Tone: [Somber and depressing, Disturbing and unsettling, Mournful and bleak]\n"
        "- Quality: [Low resolution, Grainy and unclear, Stylized rendering with dark themes]\n"
        "- High Actions: [Stillness of contaminated waters, Flies buzzing around, Algae bubbling ominously]\n"
        "- Gestures: [Insects crawling over refuse, Dead fish floating, Leaves in stagnant water]\n"
        "- Time of Day: [Midday under oppressive clouds, Late afternoon with fading light, Early morning fog]\n"
        "- Background Objects: [Rusted metal scraps, Scattered trash, Dead vegetation]\n"
        "- Camera Configuration: [Standard lens for a wide view, Macro lens for close-up decay, Wide-angle lens for pollution spread]\n"
        "- Details: [Grimy textures of algae, Dark reflections in the water, Blurred outlines of dead animals]\n"
        "- Mood/Tone: [Reflective of despair, Dark and haunting, Gloomy and melancholic]\n"
        "- Other Details: [Capture the stillness of polluted water, Highlight the absence of life, Focus on the oppressive atmosphere]."
    )

    # Call the function to generate a response based on the pre_prompt
    aria_response = ask_aria(pre_prompt)
    print(aria_response)  # Now the pre_prompt includes the user's prompt directly

    # Format the aria_response into a scene description, if necessary
    # This part would depend on how you want to structure aria's response
    
    return jsonify({
        'status': 'success', 
        'message': 'Prompt received', 
        'refinedPrompt': pre_prompt, 
        'ariaResponse': aria_response
    })



if __name__ == "__main__":
    test_database_connection()  # Call the test connection function
    app.run(debug=True)
