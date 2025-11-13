import os
from functions.utils import try_except, abs_path, merge_paths 

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
 