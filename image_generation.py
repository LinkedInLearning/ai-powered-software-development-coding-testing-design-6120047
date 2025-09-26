from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
client = OpenAI()

result = client.images.generate(
    model="dall-e-3",
    prompt="A cat wearing a suit and tie, using linkedin to find a job.",
    size="1024x1024"
)

print(result.data[0].url)