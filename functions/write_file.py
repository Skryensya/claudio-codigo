import os
from functions.utils import try_except, abs_path, merge_paths  

def write_file(working_directory, file_path, content): 
    working_directory = abs_path(working_directory)
    target_path = merge_paths(working_directory, file_path)
 
    if not target_path.startswith(working_directory):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
  
    parent_dir = os.path.dirname(target_path)
    exists = try_except(os.path.exists, parent_dir)

    if exists is not True:   
        created = try_except(os.makedirs, parent_dir)
        if isinstance(created, str) and created.startswith("Error"):
            return created  

 
    try:
        with open(target_path, "w") as f:
            result = try_except(f.write, content)
            if isinstance(result, str) and result.startswith("Error"):
                return result
    except Exception as e:
        return f"Error: {e}"

    return f'Successfully wrote to "{target_path}" ({len(content)} characters written)'
