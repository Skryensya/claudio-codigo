import os
from functions.utils import try_except, abs_path, merge_paths 
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    working_directory = abs_path(working_directory)
    target_path = merge_paths(working_directory, file_path)
 
    if not target_path.startswith(working_directory):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
  
    if not  os.path.exists(target_path):
        return f'Error: File "{file_path}" not found.'
   
    is_dot_py = target_path[-3:] == ".py"
    if not is_dot_py:
        return f'Error: "{file_path}" is not a Python file.'
    
 
    
    try:
        completed_process = subprocess.run(["uv","run",  target_path, *args], capture_output=True,
        timeout=30)
        exit_code = completed_process.returncode
        STDOUT = completed_process.stdout
        STDERR = completed_process.stderr

        response= []

        if(exit_code != 0):
            response.append(f"Process exited with code {exit_code}")

        if len(STDOUT) > 0:
            response.append(f"STDOUT: {STDOUT.decode('utf-8')}")
        
        if len(STDERR) > 0:
            response.append(f"STDERR: {STDERR.decode('utf-8')}")
            
        if len(STDOUT) == 0 and len(STDERR) == 0:
            response.append("No output produced.")
       
        return  "\n".join(response)
    except Exception as e:
        return f"Error: executing Python file: {e}"

     
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run the selected python file with the given arguments.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path the file to run is located, it must be relative to the working directory. If not provided, it'll give an error.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Array of arguments that must be passed to the function",
                items=types.Schema(type=types.Type.STRING),
            ),
            
        },
    ),
)