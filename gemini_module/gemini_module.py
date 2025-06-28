from google import genai 
from google.genai import types

def create_user_content(prompt):
    content = types.Content(
            role="user",
            parts=[types.Part.from_text(text=prompt)]
        )
    return content