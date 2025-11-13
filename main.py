import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

def main():
    arguments = sys.argv[1:]
    if(len(arguments) == 0):
        print("Error: a prompt was not provided")
        sys.exit(1)

    user_prompt = arguments[0]
    flags = arguments[1:]
    is_verbose = True if "--verbose" in arguments else False
    print(flags, is_verbose)
  

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    client = genai.Client(api_key=api_key)
    responde = client.models.generate_content(
        model='gemini-2.0-flash-001', contents=messages
    )
    print("===============================")
    print(responde.text)
    print("===============================")
    if(is_verbose):
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {responde.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {responde.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
