import os
import pathlib

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
class FileInfo:
    def __init__(self, name, file_size, is_dir):
        self.name = name 
        self.file_size = file_size
        self.is_dir = is_dir
    
    def __repr__(self):
        return f"- {self.name}: file_size={self.file_size} bytes, is_dir={self.is_dir}\n"

