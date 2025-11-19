from functions.get_files_info import get_files_info
from functions.run_python_file import run_python_file
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from google.genai import types

def call_function(function_call_part, verbose=False):
    function_name = function_call_part.name
    function_args = function_call_part.args
    if verbose:
        print(f"Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")
    
    functions_dictionary = {
        "get_files_info": get_files_info,
        "run_python_file": run_python_file,
        "get_file_content": get_file_content,
        "write_file": write_file
    }

    if function_name in functions_dictionary.keys():
        print(function_name)
        fn = functions_dictionary[function_name]
        import inspect
        sig = inspect.signature(fn)
        params = list(sig.parameters.keys())
        
        args = ["./calculator"]
        for param in params[1:]:  # Skip first param (working_directory)
            args.append(function_args.get(param, []))
        
        function_result = fn(*args)
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": function_result},
                )
            ],
        )
    else:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )