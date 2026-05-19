TOOL_REGISTRY = {}


def tool(name=None, description="", parameters=None):
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


def get_tool_call_map(name=None):
    """Return a single function if name is given, otherwise return the full name->fn dict."""
    if name:
        return TOOL_REGISTRY[name]["fn"]
    return {name: entry["fn"] for name, entry in TOOL_REGISTRY.items()}
