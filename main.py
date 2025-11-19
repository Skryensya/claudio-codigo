import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
from functions.get_files_info import schema_get_files_info
from functions.run_python_file import schema_run_python_file
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.call_function import call_function

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
    i = 0
    try:
        while i <= 10:
            responde = client.models.generate_content(
                model='gemini-2.0-flash-001',
                contents=messages, 
                config=types.GenerateContentConfig( tools=[available_functions], system_instruction=system_prompt),
            )
            candidates = responde.candidates
            for candidate in candidates:
                messages.append(types.Content(role="agent", parts=[types.Part(text=candidate.content)]))

            print("===============================")
            print(responde.text)
            if(responde.function_calls != None):
                for function_call_part in responde.function_calls:
                    function_call_result = call_function(function_call_part, is_verbose)
                response = function_call_result.parts[0].function_response.response
                if not (response):
                    raise Exception("THE FUNTION CALL DID NOT RETURN ANYTHING, ERROR")
                else: 
                    messages.append(types.Content(role="agent", parts=[types.Part(text=response)]))
                    print(f"-> {response['result']}") 
                
            print("===============================")
            if(is_verbose):
                print(f"User prompt: {user_prompt}")
                print(f"Prompt tokens: {responde.usage_metadata.prompt_token_count}")
                print(f"Response tokens: {responde.usage_metadata.candidates_token_count}")
            i+= 1
    except Exception as e:
        raise Exception(e)

if __name__ == "__main__":
    main()
