from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
client = OpenAI()

input_email = input("Enter the initial text for the email: ")

response = client.responses.create(
    model="gpt-5",
    input=f"""
    Here is an email that is potentially written in an unprofessional,
    even offensive tone. Your job is to rewrite it in a professional tone.
    Respond with ONLY the email text: {input_email}
    """,
)

print("Here is the rewritten email:\n")
print(response.output_text)
