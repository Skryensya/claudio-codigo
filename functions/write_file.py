import os
from functions.utils import try_except, abs_path, merge_paths  
from google.genai import types

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


schema_write_file =   types.FunctionDeclaration(
    name="write_file",
    description="Writes to a specified file the specified content",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path the file to read is located, it must be relative to the working directory. If not provided, it'll give an error.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="the content of the given file, what should be written in the file.",
            ),
        },
    ),
)