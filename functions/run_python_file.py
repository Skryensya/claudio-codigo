import os
from functions.utils import try_except, abs_path, merge_paths 
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    working_directory = abs_path(working_directory)
    target_path = merge_paths(working_directory, file_path)
 
    if not target_path.startswith(working_directory):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    parent_dir = os.path.dirname(target_path)
    exists = try_except(os.path.exists, parent_dir)

    if not exists:
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
       
        return (
            completed_process,
            f"Process exited with code {exit_code}\n"
            f"STDOUT: {STDOUT}\n"
            f"STDERR: {STDERR}\n"
        )
    except Exception as e:
        return f"Error: {e}"

     
    pass