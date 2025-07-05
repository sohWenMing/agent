from google import genai 
from google.genai import types



def init_client(api_key):
    try:
        assert(len(api_key) != 0)
        client = genai.Client(api_key=api_key)
        # init the client, will be re used for each request
        return client, True
    except:
        return None, False

def create_user_content(prompt):
    content = types.UserContent(
            parts=[types.Part.from_text(text=prompt)]
        )
    return content    
