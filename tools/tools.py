import os
import json
import requests
import subprocess
from pathlib import Path
from datetime import datetime

file_encoding = 'utf-8'

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_date",
            "description": "Get the current date",
            "parameters": {"type": "object", "properties": {}}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "os_bash",
            "description": "Execute command line commands on this machine",
            "parameters": {
                "type": "object",
                "properties": {
                    "cmd": {"type": "string", "description": "Executable commands compatible with the current system"}
                },
                "required": ["cmd"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "dir_location",
            "description": "Get the current directory location",
            "parameters": {"type": "object", "properties": {}}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "dir_ls",
            "description": "Obtain a list of all files (including folders) in the current directory",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Complete file system path"},
                },
                "required": ["path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "file_create",
            "description": "Create a empty file in the specified file system directory",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Complete file system path"},
                    "filename": {"type": "string", "description": "File name"},
                },
                "required": ["path", "filename"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "file_append",
            "description": "Append content to the specified filepath",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {"type": "string", "description": "Complete file system path"},
                    "content": {"type": "string", "description": "Content to be written"},
                },
                "required": ["filepath", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "file_write",
            "description": "When the specified file path does not exist, create a file and write content into it, or choose to overwrite the content in the file",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {"type": "string", "description": "Complete file system path"},
                    "content": {"type": "string", "description": "Content to be written"},
                    "overwrite": {"type": "bool", 'default':False, "description": "Is it mandatory to overwrite"},
                },
                "required": ["filepath", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "file_read",
            "description": "Read the file content from the specified filepath",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {"type": "string", "description": "Complete file system path"}
                },
                "required": ["filepath"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "file_read_lines",
            "description": "Read the content of the file from the specified filepath from the start line to the end line, and return an array where each line of content serves as an array element",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {"type": "string", "description": "Complete file system path"},
                    "startline": {"type": "number", "description": "The starting line number or single line number read. Undefined reading all"},
                    "endline": {"type": "number", "description": "The end row number read must be greater than the start row number"}
                },
                "required": ["filepath"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_ip_info",
            "description": "Obtain the geographical location information of the specified IP. If no IP is specified, obtain the current geographical location information",
            "parameters": {
                "type": "object",
                "properties": {
                    "ip": {"type": "string", "description": "IPv4 IP address; return location information if not defined"}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_ip",
            "description": "Get the current network IP",
            "parameters": {"type": "object", "properties": {}}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "dir_create",
            "description": "Create a folder in the specified path",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Complete file system new folder path"},
                },
                "required": ["path"]
            }
        }
    }
]


def get_date():
    return datetime.now().strftime("%Y-%m-%d")


def get_ip():
    try:
        response = requests.get("https://ifconfig.me", timeout=100)
        response.raise_for_status()
        return response.text.strip()
    except requests.exceptions.RequestException as e:
        return f"请求失败: {e}"


def get_ip_info(ip=None):
    if ip is None:
        url = f"https://ipapi.co/json/"
    else:
        url = f"https://ipapi.co/{ip}/json/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Referer': 'https://www.google.com/'
    }
    try:
        response = requests.get(url, headers=headers, timeout=100)
        response.raise_for_status()
        return str(response.json())
    except requests.exceptions.RequestException as e:
        return f"请求失败: {e}"


def os_bash(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True,
                            text=True, encoding=file_encoding, errors='ignore')
    if result.returncode != 0:
        return result.stderr
    return result.stdout


def dir_location():
    return os.getcwd()


def dir_ls(path):
    result = []
    for item in os.scandir(path):
        obj = {'filename': item.name, 'type': 'unkonw'}
        if item.is_dir():
            obj['type'] = 'dir'
        if item.is_file():
            obj['type'] = 'file'
        result.append(obj)
    return json.dumps(result)


def file_create(path, filename):
    file_path = Path(path) / filename
    if file_path.exists():
        return 'Error: The File Exists'
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.touch()
    return 'ok'


def file_append(filepath, content):
    file_path = Path(filepath)
    if not file_path.exists():
        return "Error: The File Not Exists"
    with file_path.open('a', encoding=file_encoding) as f:
        f.write(content)
    return "ok"


def file_read(filepath):
    file_path = Path(filepath)
    if not file_path.exists():
        return json.dumps({'msg': 'Error: The File Not Exists'})
    content = file_path.read_text(encoding=file_encoding)
    return json.dumps({'msg': 'ok', 'content': content})


def file_write(filepath, content, overwrite:False):
    file_path = Path(filepath)
    if file_path.exists():
        if not overwrite:
            return "Error: The File Exists"
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content, encoding=file_encoding)
    return 'ok'


def file_read_lines(filepath, startline=None, endline=None):

    file_path = Path(filepath)
    if not file_path.exists():
        return json.dumps({'msg': 'Error: The File Not Exists'})

    content = []
    if startline is not None:
        if endline is not None:
            if endline < startline:
                return json.dumps({'msg': 'Fail Arg: endline < startline'})
        else:
            endline = startline

        with open(file_path, 'r', encoding=file_encoding) as f:
            for current_num, line in enumerate(f, 1):
                if startline <= current_num <= endline:
                    content.append(line.strip())
                elif current_num > endline:
                    break
    else:
        with open(file_path, 'r', encoding=file_encoding) as f:
            for line in f:
                content.append(line)

    return json.dumps({'msg': 'ok', 'content': content})


def dir_create(path):
    path = Path(path)
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)
    return 'ok'


def file_insert(filepath, line, content):
    pass

def file_update_lines(filepath, array):
    pass

def file_delete_lines(filepath, array):
    pass


TOOL_CALL_MAP = {
    # 命令行
    "os_bash": os_bash,

    # 简易工具
    "get_date": get_date,

    # 网络工具
    'get_ip': get_ip,
    'get_ip_info': get_ip_info,

    # 目录操作
    "dir_ls": dir_ls,
    "dir_create": dir_create,
    "dir_location": dir_location,

    # 文件操作
    "file_read": file_read,
    "file_write": file_write,
    "file_create": file_create,
    "file_append": file_append,
    "file_read_lines": file_read_lines,
    "file_insert": file_insert,
    "file_update_lines": file_update_lines,
    "file_delete_lines": file_delete_lines,
}
