import os

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