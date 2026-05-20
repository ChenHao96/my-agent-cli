import json
import os
from pathlib import Path

from .registry import tool, check_path_safe


@tool(description="Get the current directory location")
def dir_location():
    return os.getcwd()


@tool(
    description="Obtain a list of all files (including folders) in the current directory",
    parameters={
        "type": "object",
        "properties": {
            "path": {"type": "string", "description": "File path; example: '.', '/home/user', 'C:/User/user'"},
        },
        "required": ["path"]
    }
)
def dir_ls(path: str):
    result = []
    for item in os.scandir(path):
        obj = {"filename": item.name, "type": "unkonw"}
        if item.is_dir():
            obj["type"] = "dir"
        if item.is_file():
            obj["type"] = "file"
        result.append(obj)
    return json.dumps(result)


@tool(
    description="Create a folder in the specified path",
    parameters={
        "type": "object",
        "properties": {
            "path": {"type": "string", "description": "Folder path; example: './foldername', '/home/user/foldername', 'C:/User/user/foldername'"},
        },
        "required": ["path"]
    }
)
def dir_create(path: str):
    dir_path = Path(path)
    if not check_path_safe(dir_path):
        return "Error: The FilePath Out of safe range, user confirmation is required"
    dir_path.mkdir(parents=True, exist_ok=True)
    return "ok"
