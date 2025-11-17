import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
from functions.get_files_info import schema_get_files_info
from functions.run_python_file import schema_run_python_file
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""




def main():
    arguments = sys.argv[1:]
    if(len(arguments) == 0):
        print("Error: a prompt was not provided")
        sys.exit(1)

    user_prompt = arguments[0]
    # flags = arguments[1:]
    is_verbose = True if "--verbose" in arguments else False
    # print(flags, is_verbose)
  

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]


    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file
        ]
    )

    client = genai.Client(api_key=api_key)
    responde = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages, 
        config=types.GenerateContentConfig( tools=[available_functions], system_instruction=system_prompt),
    )
    print("===============================")
    print(responde.text)
    if(responde.function_calls != None):
        for function_call_part in responde.function_calls:
            print(f"Calling function: {function_call_part.name}({function_call_part.args})")
        
    print("===============================")
    if(is_verbose):
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {responde.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {responde.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
