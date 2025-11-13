import os
from functions.utils import try_except, abs_path, merge_paths 
from config import MAX_CHAR_LIMIT


def get_file_content(working_directory, file_path):
    working_directory = abs_path(working_directory)
    target_path = merge_paths(working_directory, file_path)

    if not target_path.startswith(working_directory):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not try_except(os.path.isfile, target_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
 
    with open(target_path, "r") as f:
        file_content_string = f.read(MAX_CHAR_LIMIT)

        char_count = len(file_content_string)
        if(char_count == MAX_CHAR_LIMIT):
            file_content_string += f'[...File "{file_path}" truncated at 10000 characters]'
            
        return file_content_string
    

    pass