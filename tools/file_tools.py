import json
import chardet
from pathlib import Path

from .registry import tool


# @tool(
#     description="Create empty file under the specified file system path, and call it when the file has no content",
#     parameters={
#         "type": "object",
#         "properties": {
#             "filepath": {"type": "string", "description": "Include the file path and filename; example: '..../test.txt'"}
#         },
#         "required": ["filepath"]
#     }
# )
# def file_create(filepath):
#     file_path = Path(filepath)
#     file_path.parent.mkdir(parents=True)
#     file_path.touch()
#     return "ok"


@tool(
    description="Read the file content from the specified filepath",
    parameters={
        "type": "object",
        "properties": {
            "filepath": {"type": "string", "description": "Include the file path and filename; example: '..../test.txt'"}
        },
        "required": ["filepath"]
    }
)
def file_read(filepath):
    file_path = Path(filepath)
    if not file_path.exists():
        return json.dumps({"msg": "Error: The File Not Exists"})
    with open(filepath, 'rb') as f:
        raw = f.read()
    enc = chardet.detect(raw)['encoding']
    content = file_path.read_text(encoding=enc)
    return json.dumps({"msg": "ok", "content": content})


@tool(
    description="Create file and write content into it; File exist choose to overwrite the content in the file",
    parameters={
        "type": "object",
        "properties": {
            "content": {"type": "string", "description": "Content to be written"},
            "filepath": {"type": "string", "description": "Include the file path and filename; example: '..../test.txt'"},
            "overwrite": {"type": ["boolean", 'null'], "description": "Is it mandatory to overwrite"}
        },
        "required": ["filepath", "content"]
    }
)
def file_write(filepath, content, overwrite=None):
    file_path = Path(filepath)
    if file_path.exists():
        if overwrite is None or overwrite == False:
            return "Error: The File Exists"
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content)
    return "ok"


@tool(
    description="Append content to the specified filepath",
    parameters={
        "type": "object",
        "properties": {
            "filepath": {"type": "string", "description": "Include the file path and filename; example: '..../test.txt'"},
            "content": {"type": "string", "description": "Content to be written"},
        },
        "required": ["filepath", "content"]
    }
)
def file_append(filepath, content):
    file_path = Path(filepath)
    if not file_path.exists():
        return "Error: The File Not Exists"
    with file_path.open("a") as f:
        f.write(content)
    return "ok"


# @tool(
#     description="Read the content of the file from the specified filepath from the start line to the end line, and return an array where each line of content serves as an array element",
#     parameters={
#         "type": "object",
#         "properties": {
#             "filepath": {"type": "string", "description": "Include the file path and filename; example: '..../test.txt'"},
#             "startline": {"type": ["integer",'null'], "minimum": 0, "description": "The starting line number or single line number read. Undefined reading all"},
#             "endline": {"type": ["integer",'null'], "minimum": 0, "description": "The end row number read must be greater than the start row number"}
#         },
#         "required": ["filepath"]
#     }
# )
# def file_read_lines(filepath, startline=None, endline=None):
#     file_path = Path(filepath)
#     if not file_path.exists():
#         return json.dumps({"msg": "Error: The File Not Exists"})

#     content = []
#     if startline is not None:
#         if endline is not None:
#             if endline < startline:
#                 return json.dumps({"msg": "Fail Arg: endline < startline"})
#         else:
#             endline = startline

#         with open(file_path, "r", encoding=FILE_ENCODING) as f:
#             for current_num, line in enumerate(f, 1):
#                 if startline <= current_num <= endline:
#                     content.append(line.strip())
#                 elif current_num > endline:
#                     break
#     else:
#         with open(file_path, "r", encoding=FILE_ENCODING) as f:
#             for line in f:
#                 content.append(line)

#     return json.dumps({"msg": "ok", "content": content})
