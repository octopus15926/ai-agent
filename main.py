from functions.run_python import schema_run_python
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file

import sys
import os

from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

from google import genai
from google.genai import types
from config import system_prompt


client = genai.Client(api_key=api_key)


available_functions = types.Tool(function_declarations=
    [
    schema_get_files_info,
    schema_get_file_content,
    schema_run_python,
    schema_write_file,
    ]
)


def main():
    if len(sys.argv) >= 2:
        user_prompt = sys.argv[1]
        if user_prompt != '':
            messages = [
            types.Content(role="user", parts=[types.Part(text=user_prompt)])
            ]
            response = client.models.generate_content(
                model='gemini-2.0-flash-001',
                contents=messages,
                config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
            )
            if len(response.function_calls) > 0:
                for call in response.function_calls:
                    print(f"Calling function: {call.name}({call.args})")
            else:
                print(response.text)

        else:
            raise Exception("Did you forget to include a question?")
            return -1
        if "--verbose" in sys.argv:
            print(f"User prompt: {user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}")



if __name__ == "__main__":
    main()
