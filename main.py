import os, sys, flags_parsing, gemini_module, functions.functions
from dotenv import load_dotenv
from google.genai import types

def parse_content(content):
    try:
        response = content.parts[0].function_response.response
        if "error" in response:
            return response["error"]
        elif "result" in response:
            return response["result"]
        else:
            raise ValueError("error looking up response dict")
    except Exception as e:
        raise ValueError(e)

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

if is_verbose:
    print("verbose mode is on - the actual prompt from the user and the metadata will be printed")

is_exit = False

available_functions=gemini_module.available_functions
call_function = functions.functions.call_function

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
        
        response = gemini_module.call_gemini_get_response(client, messages)
        metadata = response.usage_metadata

        res_text = ""
        
        function_calls = response.function_calls
        if function_calls != None:
            for call in function_calls:
                content = call_function(call, is_verbose)
                res_text += parse_content(content)

        else:
            res_text = response.text

        print(res_text)

        if is_verbose == True:
            print("prompt tokens:", metadata.prompt_token_count)
            print("Response tokens:", metadata.candidates_token_count)


