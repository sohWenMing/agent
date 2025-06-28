import os, sys, flags_parsing, gemini_module
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if len(api_key) == 0:
    print("api key could not be found - exiting")
    sys.exit(1)

"""
only for debugging purposes, uncomment if required
print("api key: ", api_key)
"""

client, is_ok = gemini_module.init_client(api_key)

if is_ok == False:
    print("there was a problem initialising the gemini client")
    sys.exit(1)
# init the client, will be re used for each request

parser = flags_parsing.Parser()
is_verbose = parser.is_verbose()
print("Is verbose: ", is_verbose)

if is_verbose:
    print("verbose mode is on - the actual prompt from the user and the metadata will be printed")

is_exit = False

messages = []

while is_exit == False:
    user_input = input("Enter prompt > ")
    if user_input.strip().upper() == "EXIT":
        print("exiting program")
        sys.exit(0)
    else:
        print("##### querying ... #####")
        prompt = user_input
        messages.append(gemini_module.create_user_content(prompt))
        
        response = client.models.generate_content(
            model="gemini-2.0-flash-lite-001",
            contents=messages,
        )
        metadata = response.usage_metadata

        print(response.text)
        if is_verbose == True:
            print("prompt tokens:", metadata.prompt_token_count)
            print("Response tokens:", metadata.candidates_token_count)

