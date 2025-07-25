import os
import subprocess
from google.genai import types

schema_run_python = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python program that accepts arguments, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the python program, relative to the working directory."
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="An array holding the arguments passed to the python program."
            ),
        },
    ),
)


def run_python_file(working_directory, file_path, args=[]):
    full_file_path = os.path.join(working_directory, file_path)
    output_string = ""
    if not os.path.abspath(full_file_path).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(full_file_path):
        return f'Error: File "{file_path}" not found.'
    if ".py" not in file_path[-3:]:
        return f'Error: "{file_path}" is not a Python file.'
    
    args.insert(0, file_path)
    args.insert(0, "python3")
    subprocess_result = None
    try:
        subprocess_result = subprocess.run(args, timeout=30, capture_output=True, cwd=working_directory)
        stdout_decoded = subprocess_result.stdout.decode('utf-8')
        stderr_decoded = subprocess_result.stderr.decode('utf-8')
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
    if stdout_decoded != "":
        output_string += f"STDOUT: {stdout_decoded}\n"
    
    if stderr_decoded != "":
        if output_string != "":
            output_string += "\n"
        output_string += f"STDERR: {stderr_decoded}\n"

    if subprocess_result.returncode != 0:
        if output_string != "":
            output_string += "\n"
        output_string += f"Process exited with code {subprocess_result.returncode}"

    if output_string == "":
        return "No output produced."

    return output_string