import os
from dotenv import load_dotenv
import logging
from deepgram.utils import verboselogs
from deepgram import DeepgramClientOptions, DeepgramClient, StreamSource, PrerecordedOptions

# Load environment variables
load_dotenv()

# Specify the audio file you want to transcribe
AUDIO_FILE = "preamble.wav"

def main():
    try:
        # STEP 1: Create a Deepgram client using the API key in the environment variables
        api_key = '5d47735668d853338fcde7dd61b230bffcd95be6'
        if not api_key:
            raise ValueError("API key not found in environment variables. Please set DEEPGRAM_API_KEY.")

        config = DeepgramClientOptions(
            verbose=verboselogs.SPAM,
        )
        deepgram = DeepgramClient(api_key, config)

        # STEP 2: Call the transcribe_file method on the client
        with open(AUDIO_FILE, "rb") as stream:
            payload: StreamSource = {
                "stream": stream,
            }
            options = PrerecordedOptions(
                model="nova-2",  # You can change the model as per your requirement
            )
            response = deepgram.listen.rest.v("1").transcribe_file(payload, options)
            print(response.to_json(indent=4))

    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    main()
