from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
client = OpenAI()

response = client.responses.create(
    model="gpt-5",
    input="Find me a recipe that includes chicken, rice, and broccoli.",
)

print(response.output_text)
