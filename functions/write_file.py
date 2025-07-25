import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes the provided content to the file located at the provided file path, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the target file, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to be written to the file.",
            ),
        },
    ),
)


def write_file(working_directory, file_path, content):
    full_file_path = os.path.join(working_directory, file_path)
    if not os.path.abspath(full_file_path).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    try:
        directory = os.path.dirname(full_file_path)
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
    except:
        return f'Error: Cannot create "{file_path}"'

    try:
        with open(full_file_path, "w") as f:
            f.write(content)
    except:
        return f'Error: Cannot write to "{file_path}"'
    
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'