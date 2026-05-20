import json
from pathlib import Path

from .registry import tool, check_path_safe

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
    if not check_path_safe(file_path):
        return "Error: The FilePath Out of safe range, user confirmation is required"
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


def line_text(text: str):
    if not text.endswith('\n'):
        text += '\n'
    return text


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
        return "Warring: Items Empty"

    file_path = Path(filepath)
    if not file_path.exists():
        return "Error: The File Not Exists"

    contents = []
    with open(filepath, "r", encoding=enc_default) as f:
        for line in f:
            contents.append({'type': 'text', 'content': line_text(line)})

    inserts = []
    for item in items:
        index = item.get('index', -1)
        text = item.get('content', '')

        if index < 0:
            continue

        match item['type']:
            case 'delete':
                contents[index]['type'] = 'delete'
            case 'insert':
                inserts.append({'index': index, 'content': text})
            case 'append':
                inserts.append({'index': index + 1, 'content': text})
            case 'update':
                contents[index]['content'] = line_text(text)

    if len(inserts) > 0:
        inserts = sorted(inserts, key=lambda x: x['index'], reverse=True)
        for item in inserts:
            contents.insert(
                item['index'], {'type': 'text', 'content': line_text(item['content'])})

    with open(filepath, "w", encoding=enc_default) as f:
        for item in contents:
            if item['type'] == 'delete':
                continue
            f.write(line_text(item['content']))

    return 'ok'
