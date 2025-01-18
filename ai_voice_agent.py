from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import openai
from TTS.api import TTS
import io
import numpy as np
from scipy.io.wavfile import write
import base64

# Set OpenAI API key from environment variable
import os

# Load environment variables from .env
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

client = openai.OpenAI()

print("\nopenai.api_key =====",openai.api_key)

# Initialize TTS and print available speakers

tts_model = TTS("tts_models/multilingual/multi-dataset/xtts_v2")

@app.post("/voice-agent/")
async def voice_assistant(file: UploadFile = File(...)):
    print("filename",file.filename)
    print("content type",file.content_type)

    # Read audio file
    audio_bytes = await file.read()

    # Transcribe audio to text using OpenAI
    audio_file = io.BytesIO(audio_bytes)
    audio_file.name = file.filename

    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file)
    
    text = transcription.text

    print("text:", text)

    # Generate response using OpenAI GPT-4
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": text}]
    )

    print("\nresponse ===== ",response)
    
    generated_text = response.choices[0].message.content

    print("\ngenerated_text:", generated_text)

    # Convert text to speech
    audio_output = tts_model.tts(text=generated_text, speaker_wav="data/recordings/hamd_recording.wav", language="en")

    print("\naudio_output1 =====",audio_output)

    # Step 1: Ensure `audio_output` is a NumPy array
    if isinstance(audio_output, list):  # If the output is a list, convert it to a NumPy array
        audio_output = np.array(audio_output, dtype=np.float32)

    # Step 2: Normalize and convert to `int16` (for WAV compatibility)
    audio_output = (audio_output * 32767).astype(np.int16)

    print("\naudio_output2 =====",audio_output)
    
    # Create a BytesIO stream for the audio
    audio_stream = io.BytesIO(audio_output)
    write(audio_stream, rate=22050, data=audio_output)  # Example rate: 22050 Hz
    audio_stream.seek(0)

    print("\naudio_stream =====",audio_stream)

    # Encode the audio as Base64
    audio_base64 = base64.b64encode(audio_stream.getvalue()).decode("utf-8")
    
    print("type(transcription) =====",type(transcription))  # Should be <class 'str'>
    print("type(generated_text) =====",type(generated_text))  # Should be <class 'str'>
    print("type(audio_base64) =====",type(audio_base64))  # Should be <class 'str'>

    # Return JSON response with Base64 audio
    return JSONResponse(
        content={
            "transcription": text,
            "response": generated_text,
            "audio": audio_base64,
        }
    )

# Run the application with: uvicorn ai_voice_agent:app --reload
