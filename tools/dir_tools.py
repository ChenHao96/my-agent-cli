import json
import os
from pathlib import Path

from .registry import tool


@tool(description="Get the current directory location")
def dir_location():
    return os.getcwd()


@tool(
    description="Obtain a list of all files (including folders) in the current directory",
    parameters={
        "type": "object",
        "properties": {
            "path": {"type": "string", "description": "Complete file system path"},
        },
        "required": ["path"]
    }
)
def dir_ls(path):
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
            "path": {"type": "string", "description": "Complete file system folder path"},
        },
        "required": ["path"]
    }
)
def dir_create(path):
    Path(path).mkdir(parents=True, exist_ok=True)
    return "ok"
