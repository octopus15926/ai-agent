import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)


def get_files_info(working_directory, directory="."):
    dir_path = os.path.join(working_directory, directory)
    directory_string = directory
    if directory == '.':
        directory_string = "current"
    result_string = ""

    if not os.path.isdir(dir_path):
        result_string += f'Error: "{directory}" is not a directory'
        return result_string

    if not os.path.abspath(dir_path).startswith(os.path.abspath(working_directory)):
        result_string += f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        return result_string
        
    contents = None
    try:
        contents = os.listdir(dir_path)
    except Exception:
        result_string += f"Error: Invalid directory path"
        return result_string
    
    result_string = f"Result for {directory_string} directory:\n"
    if contents:
        for file in contents:
            file_path =  f"{dir_path}/{file}"
            try:
                file_size = os.path.getsize(file_path)
                file_is_dir = os.path.isdir(file_path)
            except:
                result_string += f"Error: Invalid file path"
                return result_string
            result_string += f"- {file}: file_size={file_size}, is_dir={file_is_dir}\n"
    return result_string