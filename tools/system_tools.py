import subprocess
from datetime import datetime

from .registry import tool, check_bash_safe


@tool(description="Get the current date")
def get_date():
    return datetime.now().strftime("%Y-%m-%d")


@tool(description="Get the current time")
def get_time():
    return datetime.now().strftime("%H:%M:%S")


@tool(description="Get the current date and time")
def get_datetime():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@tool(
    description="Execute command line commands on this machine",
    parameters={
        "type": "object",
        "properties": {
            "cmd": {"type": "string", "description": "Executable commands compatible with the current system; Like Windows:'findstr', Linux/Mac:'grep'"}
        },
        "required": ["cmd"]
    }
)
def os_bash(cmd: str):
    if not check_bash_safe(cmd):
        return "Error: The command Out of safe range, user confirmation is required"
    result = subprocess.run(cmd, shell=True, capture_output=True,
                            text=True, encoding="utf-8", errors="ignore")
    if result.returncode != 0:
        return result.stderr
    return result.stdout
