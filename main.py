import json
from pathlib import Path
from openai import OpenAI

from tools import get_tools, get_tool_call_map

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


kwargs = {
    "stream": False,
    "messages": messages,
    "model": "qwen/qwen3.5-9b",
    "extra_body": {"thinking": {"type": "disable"}}
}

_tools = get_tools()
if len(_tools) > 0:
    kwargs['tools'] = _tools
    kwargs['tool_choice'] = "auto"

if reasoning_effort != "off":
    kwargs['reasoning_effort'] = reasoning_effort
    kwargs['extra_body'] = {"thinking": {"type": "enable"}}


client = OpenAI(
    api_key="llm-studio",
    base_url="http://localhost/v1",
)


def is_empty_or_whitespace(s: str) -> bool:
    return not s or s.isspace()


def append_assistant_message(messageObj):
    msg = {'role': 'assistant'}
    if len(messageObj.content) > 0:
        msg.update({'tool_calls': messageObj.tool_calls})
    if not is_empty_or_whitespace(messageObj.content):
        msg.update({'content': messageObj.content.strip()})
    if not is_empty_or_whitespace(messageObj.reasoning_content):
        msg.update({'reasoning_content': messageObj.reasoning_content.strip()})
    messages.append(msg)


def run(messages):

    completion_tokens = 0
    prompt_tokens = 0
    total_tokens = 0

    while True:
        response = client.chat.completions.create(**kwargs)
        total_tokens += response.usage.total_tokens
        prompt_tokens += response.usage.prompt_tokens
        completion_tokens += response.usage.completion_tokens

        print(
            f"\033[36m{response.model_dump_json(indent=2, ensure_ascii=False)}\033[0m")

        for _, choice in enumerate(response.choices):
            messageObj = choice.message
            append_assistant_message(messageObj)
            match choice.finish_reason:
                case "tool_calls":
                    for _, tool in enumerate(messageObj.tool_calls):
                        # if tool.function.name == "os_bash":
                        #     # TODO：开启一个新的请求来判断用户是否允许执行
                        #     # 1. 本次操作
                        #     # 2. 当前会话
                        #     # 3. 其他
                        #     break

                        tool_function = get_tool_call_map(tool.function.name)
                        try:
                            tool_result = tool_function(
                                **json.loads(tool.function.arguments))
                        except Exception as e:
                            tool_result = f"{tool.function.name}({tool.function.arguments[:30]}) error: {e}"
                            print(f"\033[31m{tool_result}\033[0m")
                        messages.append(
                            {"role": "tool", "tool_call_id": tool.id, "content": tool_result})
                    break
                case "stop":
                    print(
                        f"\033[33m >> prompt:{prompt_tokens}, completion:{completion_tokens}, total:{total_tokens}\033[0m")
                    return


while True:
    content = input(">> ")
    messages.append({"role": "user", "content": content})
    run(messages)
    print(f"\033[33m >> {messages[-1]['reasoning_content']}\033[0m")
    print(messages[-1]['content'])
