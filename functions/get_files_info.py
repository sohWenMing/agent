import os
import pathlib

def get_files_info(working_directory, directory=None):
    """
    the main idea behind this function is that is should:
    1. check if the directory param given is within the working directory
        this means if ../ is given, should return error
    """

    if directory == "../":
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    # if trying to navigate to parent, don't allow 

    if directory == None:
        directory = "."
    # default to current directory if none is given

    relative_path = pathlib.Path(directory)
    base_dir = pathlib.Path(working_directory)

    work_dir_abs_path = base_dir.resolve()
    resolved_path = (base_dir / relative_path).resolve()


    entries = os.listdir(work_dir_abs_path)

    for entry in entries:
        full_path = os.path.join(working_directory, entry)
        if full_path == str(resolved_path):
            if os.path.isdir(full_path):
                return "ok, this is a directory in the cwd"
            else:
                return f'Error: "{directory}" is not a directory'

    return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

class FileInfo:
    def __init__(self, name, file_size, is_dir):
        self.name = name 
        self.file_size = file_size
        self.is_dir = is_dir
    
    def __repr__(self):
        return f"{self.name}: file_size={self.file_size} bytes, is_dir={self.is_dir}"
