import os
from pathlib import Path

TOOL_REGISTRY = {}


def tool(name: str = None, description: str = "", parameters: dict = None):
    """Decorator: bind a function with its OpenAI tool schema and register it."""
    def decorator(fn):
        nonlocal name
        name = name or fn.__name__
        TOOL_REGISTRY[name] = {
            "schema": {
                "type": "function",
                "function": {
                    "name": name,
                    "description": description,
                    "parameters": parameters or {"type": "object", "properties": {}}
                }
            },
            "fn": fn
        }
        return fn
    return decorator


def get_tools():
    return [entry["schema"] for entry in TOOL_REGISTRY.values()]


def get_tool_call_map(name: str = None):
    """Return a single function if name is given, otherwise return the full name->fn dict."""
    if name:
        return TOOL_REGISTRY[name]["fn"]
    return {name: entry["fn"] for name, entry in TOOL_REGISTRY.items()}


def get_current_work_path():
    # TODO: 返回用户选择的工作目录
    # 默认返回当前目录
    return os.getcwd() + "/test"


safe_path_set = set()
def check_path_safe(path: Path):
    safe_path = Path(get_current_work_path())
    resolve_path = path.resolve()
    if resolve_path.is_relative_to(safe_path):
        return True
    else:
        if resolve_path in safe_path_set:
            return True
        # TODO: 判断地址是否安全授权过
        pass
    return False


safe_cmd_set = set()
def check_bash_safe(cmd):
    if cmd in safe_cmd_set:
        return True
    else:
        # TODO: 判断命令是否可以执行
        pass
    return False
