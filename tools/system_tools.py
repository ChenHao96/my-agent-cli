import subprocess
from datetime import datetime

from .registry import tool


@tool(description="Get the current date")
def get_date():
    return datetime.now().strftime("%Y-%m-%d")


@tool(description="Get the current time")
def get_time():
    return datetime.now().strftime("%H:%M:%S")


@tool(
    description="Execute command line commands on this machine",
    parameters={
        "type": "object",
        "properties": {
            "cmd": {"type": "string", "description": "Executable commands compatible with the current system"}
        },
        "required": ["cmd"]
    }
)
def os_bash(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True,
                            text=True, encoding="utf-8", errors="ignore")
    if result.returncode != 0:
        return result.stderr
    return result.stdout
