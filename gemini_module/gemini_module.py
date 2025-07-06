from google import genai 
from google.genai import types

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""


def call_gemini_get_response(client, messages):
        response = client.models.generate_content(
        model="gemini-2.0-flash-lite-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt)
        )
        return response 


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

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="reads the content of the specified file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="the file from which to read, relative to the current working directory",
            ),
        },
    ),
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="runs the specified file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="the file to run, relative to the current working directory",
            ),
        },
    ),
)
schema_write_file = types.FunctionDeclaration(
    name="write_file_content",
    description="writes or overwrites content to the specified file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="the file to run, relative to the current working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="the content that is to be written to the file",
            ),
        },
    ),
)

available_functions=types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]
)