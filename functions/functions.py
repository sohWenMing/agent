import os
import pathlib
import subprocess

########## Class Definitions ##########
class FileInfo:
    def __init__(self, name, file_size, is_dir):
        self.name = name 
        self.file_size = file_size
        self.is_dir = is_dir
    
    def __repr__(self):
        return f"- {self.name}: file_size={self.file_size} bytes, is_dir={self.is_dir}\n"


########## Public Funcs ##########
def call_function(function_call_part, verbose=False):
    working_directory = "./calculator"
    try:
        func, args, is_get_func_success  = get_func_and_args(function_call_part)
        if is_get_func_success == False:
            raise ValueError(f"function {function_call_part.name} does not exist")

        if verbose==True:
            print(f"Calling function: {function_call_part.name}({function_call_part.args})")
        else:
            print(f" - Calling function: {function_call_part.name}")

        if func == write_file_content:
            return func(working_directory, 
                        args["file_path"], args["content"])

        elif func == get_files_info:
            if args == {}:
                args["file_path"] = "."
            return func(working_directory, args["file_path"])
        else:
            return func(working_directory, args["file_path"])
    except Exception as e:
        return f"Error: {e}"

def get_func_and_args(function_call_part):
    name = function_call_part.name
    args = function_call_part.args

    if name == "get_files_info":
        return get_files_info, args, True
    elif name == "get_file_content":
        return get_file_content, args, True
    elif name == "run_python_file":
        return run_python_file, args, True
    elif name == "write_file_content":
        return write_file_content, args, True
    else:
        return None, None, False


def run_python_file(working_directory, file_path):
    if file_path.startswith(".."):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    resolved_path = __get_resolved_path(working_directory, file_path)

    if os.path.exists(resolved_path) == False:
        return f'Error: File "{file_path}" not found'
    
    if file_path.endswith(".py") == False:
        return f'Error: "{file_path}" is not a Python file.'
    return __run_subprocess(resolved_path)




def write_file_content(working_directory, file_path, content):

    if file_path.startswith(".."):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
    resolved_path = __get_resolved_path(working_directory, file_path)
    write_res = __write_to_file(resolved_path, content)
    return write_res

def get_file_content(working_directory, file_path):
    if   file_path.startswith(".."):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    returned_string_from_check, is_check_success = __check_resolved_path(working_directory, file_path)

    if is_check_success == False:
        return returned_string_from_check

    resolved_path = returned_string_from_check

    return __read_file_max_chars(resolved_path, 10000)

def get_files_info(working_directory, directory=None):
    """
    working_directory refers to the directory within which the file
    which calls the function is contained

    directory is the actual directory where we want to get info from 
    """

    if directory == "../":
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    # if trying to nav to directory outside of working directory disallow

    if directory == None:
        directory = "."
    # default to current directory if none is given

    resolved_path = __get_resolved_path(working_directory, directory)
    # gets the working dir + the additional directory input 

    if os.path.exists(resolved_path) == False:
        return f'error: "{resolved_path} does not exist'
    # if the directory path does not exist, exit and return error

    if os.path.isdir(resolved_path) == False:
        return f'Error: "{directory}" is not a directory'
    # if the the file is not a directory, exit early 

    entries = os.listdir(resolved_path)
    # gets the list of all files and directories within the folder

    return __get_dir_info(resolved_path, entries)


########### Private funcs ###########

def __run_subprocess(file_path):
    args = ["python3", file_path]
    try:
        completed_process = subprocess.run(args, capture_output=True, timeout=30)
        returned_string =   (
                                "RESULTS: \n" +  
                                f"STDOUT: {completed_process.stdout}\n" + 
                                f"STDERR: {completed_process.stderr}\n" 
                            )
        if completed_process.returncode != 0:
            returned_string += f'Process exited with code "{completed_process.returncode}\n"'
        if completed_process.stdout == None:
            returned_string += "No output produced.\n"
        return returned_string

    except Exception as e:
        return f'Error: executing Python file: {e}'

def __check_resolved_path(working_directory, file_path):
    if   file_path.startswith(".."):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory', False
    resolved_path = __get_resolved_path(working_directory, file_path)
    # gets the working dir + the additional directory input 

    if os.path.exists(resolved_path) == False:
        return f'error: "{file_path}" does not exist', False
    # if the directory path does not exist, exit and return error

    if  os.path.exists(resolved_path) == False:
        return f'Error: File not found or is not a regular file: "{file_path}"', False
    # if the file does not exist, exit early 

    if os.path.isdir(resolved_path) == True:
        return f'Error: File not found or is not a regular file: "{file_path}"', False
    # if the file is a directory, exit early 

    return resolved_path, True

def __write_to_file(path, content):
    try:
        with open(path, "w") as f:
            chars_written = f.write(content)
            return f'Successfully wrote to "{path}" ({chars_written} characters written)'
    except Exception as e:
        return f"Error: {e}"



def __read_file_max_chars(filepath, max_chars):
    try:
        with open(filepath, "r") as f:
            file_content_string = f.read(max_chars)
            return file_content_string
    except Exception as e:
        return f"Error: {str(e)}"

def __get_dir_info(resolved_path, entries):
    returned_string = f"Result for current directory:\n" 

    for entry in entries:
    # function is not built to be recursive, so will only look within one level 
        full_path = os.path.join(resolved_path, entry)
        file_size = os.path.getsize(full_path)
        is_dir = os.path.isdir(full_path)

        file_info = FileInfo(entry, file_size, is_dir)
        returned_string += repr(file_info)
    
    return returned_string

def __get_resolved_path(working_directory, directory):
    base_dir = pathlib.Path(os.path.abspath(working_directory))
    relative_path = pathlib.Path(directory)

    resolved_path = str((base_dir / relative_path).resolve())
    return resolved_path

"""
example returned string:

- README.md: file_size=1032 bytes, is_dir=False
- src: file_size=128 bytes, is_dir=True
- package.json: file_size=1234 bytes, is_dir=False

"""
