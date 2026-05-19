import json
from pathlib import Path

from .registry import tool

enc_default = 'utf-8'


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
def file_read(filepath: str):
    file_path = Path(filepath)
    if not file_path.exists():
        return json.dumps({"msg": "Error: The File Not Exists"})
    content = file_path.read_text(encoding=enc_default)
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
def file_write(filepath: str, content: str, overwrite: bool = None):
    file_path = Path(filepath)
    if file_path.exists():
        if overwrite is None or overwrite == False:
            return "Error: The File Exists"
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content, encoding=enc_default)
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
def file_append(filepath: str, content: str):
    file_path = Path(filepath)
    if not file_path.exists():
        return "Error: The File Not Exists"
    with file_path.open("a", encoding=enc_default) as f:
        f.write(content)
    return "ok"


@tool(
    description="""Modify the content of a file line from the specified file path, including inserte lines, append lines, delete lines, and update lines
    example 1: delete lines
        filepath: '..../test.txt'
        items: [{'type':'delete','index':2},{'type':'delete','index':3},{'type':'delete','index':5}]
    example 2: update lines
        filepath: '..../test.txt'
        items: [{'type':'update','index':2,'content','update content....'}]
    example 3: insert/append lines
        filepath: '..../test.txt'
        items: [{'type':'insert','index':2,'content','content....'},{'type':'append','index':2,'content','content....'}]
    """,
    parameters={
        "type": "object",
        "properties": {
            "filepath": {"type": "string", "description": "Include the file path and filename; example: '..../test.txt'"},
            "items": {
                "type": "array",
                "description": "The modified lines",
                "items": {
                    "type": "object",
                    "properties": {
                        "index": {
                            "type": "integer",
                            "minimum": 0,
                            "description": "The line number; The first row is represented by 0"
                        },
                        "type": {
                            "type": "string",
                            "enum": ["delete", "insert", "append", "update"],
                            "description": """Modify type. 
                                insert: It will write content before the specified line number
                                append: It will write content after the specified line number
                                delete: Delete row the specified line number
                                update: Update row content the specified line number
                            """
                        },
                        "content": {
                            "type": ["string", "null"],
                            "description": "Line content; When type is 'delete', it can be null"
                        }
                    },
                    "required": ["index", "type"]
                }
            },
        },
        "required": ["filepath", "items"]
    }
)
def file_modify_lines(filepath: str, items: list):

    if len(items) <= 0:
        return "no changed"

    file_path = Path(filepath)
    if not file_path.exists():
        return "Error: The File Not Exists"

    contents = []
    with open(filepath, "r", encoding=enc_default) as f:
        contents = f.readlines()

    dels = []
    inserts = []
    for item in items:
        index = item.get('index', -1)
        text = item.get('content', '')

        if index < 0:
            continue

        match item['type']:
            case 'delete':
                dels.append(index)
                break
            case 'insert':
                inserts.append({'index': index, 'content': text})
                break
            case 'append':
                inserts.append({'index': index + 1, 'content': text})
                break
            case 'update':
                if not text.endswith('\n'):
                    text += '\n'
                contents[index] = text
                break

    # TODO: 混合修改时存在问题

    if len(dels) > 0:
        for idx in sorted(dels, reverse=True):
            del contents[idx]

    if len(inserts) > 0:
        inserts = sorted(inserts, key=lambda x: x['index'], reverse=True)
        for item in inserts:
            new = item['content']
            if not new.endswith('\n'):
                new += '\n'
            contents.insert(item['index'], new)

    with open(filepath, "w", encoding=enc_default) as f:
        for content in contents:
            if not content.endswith('\n'):
                content += '\n'
            f.write(content)

    return 'ok'
