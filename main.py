import os, string_parsing, sys
from dotenv import load_dotenv
from google import genai



load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

"""
only for debugging purposes, uncomment if required
print("api key: ", api_key)
"""
arg_strings = sys.argv[1:]
if len(arg_strings) == 0:
    print("You need to supply a prompt! Exiting program")
    sys.exit(1)

prompt = string_parsing.join_with_space(arg_strings)
print("Prompt: ", prompt)


client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model="gemini-2.0-flash-lite-001",
    contents=prompt,
)

metadata = response.usage_metadata

print(response.text)
print("prompt tokens:", metadata.prompt_token_count)
print("Response tokens:", metadata.candidates_token_count)
