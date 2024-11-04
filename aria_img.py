import base64
import requests
from config import ARIA_API_KEY
from textwrap import dedent

def analyze_image(base64_image):
    payload = {
        "model": "aria",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
                    {"type": "text", "text": dedent("""\
                    <image>\nThis is an image of a polluted river. Focus on the negative aspects of the scene, highlighting the presence of algae and decay while considering the following options. Please choose one option from each parameter:

                    - Subject: [Toxic algae blooms, Dead fish, Insects infesting the area]
                    - Activity: [Pollution effects, Decomposition, Insect swarming]
                    - Background: [Lifeless banks, Trash-filled shores, Industrial wasteland]
                    - Light: [Dull overcast light, Harsh artificial lighting, Gloomy twilight]
                    - Angle: [Ground level with a grim perspective, Aerial view showing pollution spread, Close-up on decay]
                    - Style: [Grim realism, Distorted interpretation, Depressing depiction]
                    - Artistic Medium: [Digital art focusing on decay, Dark watercolor, Oil painting with heavy strokes]
                    - Color Palette: [Sickly greens and browns, Dark and murky shades, Muted, lifeless colors]
                    - Exclusions: [Natural beauty, Wildlife, Clear water]
                    - Aspect Ratio: [16:9, 4:3, Square]
                    - Character Details: [None specified, Dead animals, Swarms of flies]
                    - Props: [Debris and trash, Stagnant water, Algae-covered rocks]
                    - Setting: [Contaminated river lined with refuse, An abandoned industrial site, A dead-end waterway]
                    - Atmosphere: [Dreary and oppressive, Stagnant and decaying, Uninviting and dark]
                    - Visual Composition: [Chaotic with a focus on pollution, Centered on decay, Distracting clutter]
                    - Emotional Tone: [Somber and depressing, Disturbing and unsettling, Mournful and bleak]
                    - Quality: [Low resolution, Grainy and unclear, Stylized rendering with dark themes]
                    - High Actions: [Stillness of contaminated waters, Flies buzzing around, Algae bubbling ominously]
                    - Gestures: [Insects crawling over refuse, Dead fish floating, Leaves floating in stagnant water]
                    - Time of Day: [Midday under oppressive clouds, Late afternoon with fading light, Early morning fog]
                    - Background Objects: [Rusted metal scraps, Scattered trash, Dead vegetation]
                    - Camera Configuration: [Standard lens for a wide view, Macro lens to capture decay up close, Wide-angle lens to show pollution spread]
                    - Details: [Grimy textures of algae, Dark reflections in the water, Blurred outlines of dead animals]
                    - Art Style: [Dark realism, Grotesque imagery, Surreal but grim]
                    - Artist Influence: [Francisco Goya, Edward Hopper, Anselm Kiefer]
                    - Mood/Tone: [Reflective of despair, Dark and haunting, Gloomy and melancholic]
                    - Other Details: [Capture the stillness of the polluted water, Highlight the absence of life, Focus on the oppressive atmosphere].

                    Provide the result in the following format only:
                    Scene 1: <description>
                    Return exactly 1 scene in that format.
                    """)}
                ]
            }
        ],
        "temperature": 0.6,
        "max_tokens": 1024,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0,
        "stream": False,
        "stop": ["<|im_end|>"],
        "image_max_size": 980,
        "split_image": True,
    }
        
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
