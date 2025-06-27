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


# client = genai.client(api_key=api_key)

# response = client.models.generate_content(
#     model="gemini-2.0-flash-lite-001",
#     contents="why is boot.dev such a great place to learn backend development? use one paragraph maximum.",
# )

# metadata = response.usage_metadata

# print(response.text)
# print("prompt tokens:", metadata.prompt_token_count)
# print("Response tokens:", metadata.candidates_token_count)
string_parsing.print_string("this is a test of a print string function")
