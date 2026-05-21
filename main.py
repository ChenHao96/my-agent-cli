import json
from pathlib import Path
from openai import OpenAI

from tools import get_tools, get_tool_call_map
from tools.dir_tools import dir_location

reasoning_effort = "off"

SYSTEM_PROMPT = "You are a helpful assistant with access to various tools."
file_path = Path(".agent/system_prompt.md")
if file_path.exists():
    SYSTEM_PROMPT = file_path.read_text(encoding='utf-8')

# USER_PROMPT = ""
# file_path = Path(".agent/user_prompt.md")
# if file_path.exists():
#     USER_PROMPT = file_path.read_text(encoding='utf-8')
# USER_PROMPT += "/nHello/n"


messages = [
    {"role": "system", "content": SYSTEM_PROMPT}
]
workPath = dir_location()
messages.append({"role": "tool", "tool_call_id": "dir_location", "content": workPath})

# TODO: 向用户确认当前工作目录是否可信
# agent_path = Path(workPath) + "/.agent/.agent.json"
# if not agent_path.exists():
#     jsonContent = "{}"
#     agent_path.parent.mkdir(parents=True, exist_ok=True)
#     agent_path.write_text(jsonContent, encoding='utf-8')
# else:
#     pass


kwargs = {
    "stream": False,
    "messages": messages,
    "model": "Qwen3.6-35B-A3B-Q4_K_M.gguf",
    "extra_body": {"thinking": {"type": "disable"}}
}

_tools = get_tools()
if len(_tools) > 0:
    kwargs['tools'] = _tools
    kwargs['tool_choice'] = "auto"

if reasoning_effort != "off":
    kwargs['reasoning_effort'] = reasoning_effort
    kwargs['extra_body'] = {"enable_thinking": False}


client = OpenAI(
    api_key="llama-cpp",
    base_url="http://localhost/v1",
)


def is_empty_or_whitespace(s: str) -> bool:
    return not s or s.isspace()


def append_assistant_message(messageObj):
    msg = {'role': 'assistant', 'content': ''}
    if not is_empty_or_whitespace(messageObj.content):
        msg.update({'content': messageObj.content.strip()})
    if messageObj.tool_calls and len(messageObj.tool_calls) > 0:
        msg.update({'tool_calls': messageObj.tool_calls})
    if hasattr(messageObj, 'reasoning_content'):
        if not is_empty_or_whitespace(messageObj.reasoning_content):
            msg.update(
                {'reasoning_content': messageObj.reasoning_content.strip()})
    messages.append(msg)


def run(messages):
    while True:
        # TODO: 移除失败的调用来压缩上下文

        response = client.chat.completions.create(**kwargs)
        print(
            f"\033[36m{response.model_dump_json(indent=2, ensure_ascii=False)}\033[0m")

        for _, choice in enumerate(response.choices):
            messageObj = choice.message
            append_assistant_message(messageObj)
            match choice.finish_reason:
                case "tool_calls":
                    for _, tool in enumerate(messageObj.tool_calls):
                        tool_function = get_tool_call_map(tool.function.name)
                        try:
                            tool_result = tool_function(
                                **json.loads(tool.function.arguments))
                        except Exception as e:
                            tool_result = f"{tool.function.name}({tool.function.arguments[:30]}) error: {e}"
                            print(f"\033[31m{tool_result}\033[0m")
                        messages.append(
                            {"role": "tool", "tool_call_id": tool.id, "content": tool_result})
                case "stop":
                    print(
                        f"\033[33m >> prompt:{response.usage.prompt_tokens}, completion:{response.usage.completion_tokens}, total:{response.usage.total_tokens}\033[0m")
                    return


while True:
    content = input(">> ")
    messages.append({"role": "user", "content": content})
    run(messages)
    reasoning_content = messages[-1].get('reasoning_content', '')
    if not is_empty_or_whitespace(reasoning_content):
        print(f"\033[33m >> {reasoning_content}\033[0m")
    print(messages[-1].get('content', ''))
