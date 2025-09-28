from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
client = OpenAI()

retro_notes = input("Copy and paste the retro notes here: ")

response = client.responses.create(
    model="gpt-5",
    input=f"""
    Here are the notes from our 5 developer team's sprint retro.
    Group them into themes (process, teamwork, tooling), summarize the main insights,
    and suggest improvement actions:
    {retro_notes}
    """,
)

print("Here are the results:\n")

print(response.output_text)
