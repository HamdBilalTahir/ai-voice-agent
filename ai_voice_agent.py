from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")
from TTS.api import TTS
import io

app = FastAPI()

# Set OpenAI API key from environment variable
import os

# Load environment variables from .env
load_dotenv()


print("\nopenai.api_key =====",openai.api_key)

# Initialize TTS

print("\nTTS Models =====",TTS().list_models())

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

    transcription = openai.audio.transcribe(model="whisper-1",
    file=audio_file)
    text = transcription.text

    print("text:", text)

    # Generate response using OpenAI GPT-4
    response = openai.Chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": text}]
    )
    generated_text = response['choices'][0]['message']['content']

    print("generated_text:", generated_text)

    # Convert text to speech
    audio_output = tts_model.tts(generated_text)

    # Create a BytesIO stream for the audio
    audio_stream = io.BytesIO(audio_output)
    audio_stream.seek(0)

    return {
        "transcription": text,
        "response": generated_text,
        "audio": StreamingResponse(audio_stream, media_type="audio/wav")
    }

# Run the application with: uvicorn ai_voice_agent:app --reload
