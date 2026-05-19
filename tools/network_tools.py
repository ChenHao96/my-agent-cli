import requests

from .registry import tool


@tool(description="Get the current network IP")
def get_ip():
    try:
        response = requests.get("https://ifconfig.me", timeout=100)
        response.raise_for_status()
        return response.text.strip()
    except requests.exceptions.RequestException as e:
        return f"error: {e}"


@tool(
    description="Obtain the geographical location information of the specified IP. If no IP is specified, obtain the current geographical location information",
    parameters={
        "type": "object",
        "properties": {
            "ip": {"type": ["string", 'null'], "description": "IPv4 IP address; return location information if not defined"}
        }
    }
)
def get_ip_info(ip: str = None):
    if ip is None:
        url = "https://ipapi.co/json/"
    else:
        url = f"https://ipapi.co/{ip}/json/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Referer": "https://www.google.com/"
    }
    try:
        response = requests.get(url, headers=headers, timeout=100)
        response.raise_for_status()
        return str(response.json())
    except requests.exceptions.RequestException as e:
        return f"error: {e}"
