import os
import config

def get_file_content(working_directory, file_path):
    dir_file_path = os.path.join(working_directory, file_path)
    result_string = ""
    if not os.path.abspath(dir_file_path).startswith(os.path.abspath(working_directory)):
        result_string += f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        return result_string
    
    if not os.path.isfile(dir_file_path):
        result_string += f'Error: File not found or is not a regular file: "{file_path}"'
        return result_string
    
    try:
        with open(dir_file_path, "r") as file:
            file_content_string = file.read(config.MAX_CHARS + 1)
            
            if len(file_content_string) > config.MAX_CHARS:
                result_string += f"{file_content_string[:config.MAX_CHARS]}\n"
                result_string += f'\n[...File "{file_path}" truncated at {config.MAX_CHARS} characters]'
            else:
                result_string += file_content_string
    except:
        result_string += f"Error: Failed to read from {file_path}"

    return result_string