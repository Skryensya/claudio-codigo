import os
from functions.utils import try_except, abs_path, merge_paths
from google.genai import types

def get_files_info(working_directory, directory="."): 
    working_directory = abs_path(working_directory)
    target_path = merge_paths(working_directory, directory)

    if not target_path.startswith(working_directory):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if not try_except(os.path.isdir, target_path):
        return f'Error: "{directory}" is not a directory'
    
    directory_tree = try_except(os.listdir, target_path)

    logs = []
    for entry in directory_tree:
        pwd = merge_paths(target_path, entry)
        size = os.path.getsize(pwd)
        is_dir = not os.path.isfile(pwd)
        log = f"- {entry}: file_size={size} bytes, is_dir={is_dir}"
        logs.append(log)
       

    return "\n".join(logs)
 

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. it has to always be there, defaults to .",
            ),
        },
    ),
)