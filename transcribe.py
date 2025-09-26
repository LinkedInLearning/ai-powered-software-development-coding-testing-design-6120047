from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI

client = OpenAI()
audio_file= open("recording.m4a", "rb")

transcription = client.audio.transcriptions.create(
    model="gpt-4o-transcribe", 
    file=audio_file
)

print(transcription.text)