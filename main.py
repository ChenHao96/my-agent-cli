import json
from pathlib import Path
from openai import OpenAI

from tools import tools, TOOL_CALL_MAP

reasoning_effort = "off"

SYSTEM_PROMPT = "You are a helpful assistant with access to various tools."
file_path = Path("./system_prompt.md")
if file_path.exists():
    SYSTEM_PROMPT = file_path.read_text(encoding = 'utf-8')

USER_PROMPT = ""
file_path = Path("./user_prompt.md")
if file_path.exists():
    USER_PROMPT = file_path.read_text(encoding = 'utf-8')
USER_PROMPT += "/nHello/n"


messages = [{"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": USER_PROMPT}]


kwargs = {
    "stream": False,
    "messages": messages,
    "model": "qwen/qwen3.5-9b",
    "extra_body": {"thinking": {"type": "disable"}}
}

if len(tools) > 0:
    kwargs['tools'] = tools
    kwargs['tool_choice'] = "auto"

if reasoning_effort != "off":
    kwargs['reasoning_effort'] = reasoning_effort
    kwargs['extra_body'] = {"thinking": {"type": "enable"}}


client = OpenAI(
    api_key="llm-studio",
    base_url="http://localhost/v1",
)


def run(messages):
    while True:
        response = client.chat.completions.create(**kwargs)
        print(response.model_dump_json(indent=2, ensure_ascii=False))

        for _, choice in enumerate(response.choices):
            messageObj = choice.message
            messages.append({'role': 'assistant', 'content': messageObj.content,
                             'reasoning_content': messageObj.reasoning_content, 'tool_calls': messageObj.tool_calls})
            match choice.finish_reason:
                case "tool_calls":
                    for _, tool in enumerate(messageObj.tool_calls):
                        tool_function = TOOL_CALL_MAP[tool.function.name]
                        try:
                            tool_result = tool_function(
                                **json.loads(tool.function.arguments))
                        except Exception as e:
                            tool_result = f"error: {e}"
                            print(tool_result)
                        messages.append(
                            {"role": "tool", "tool_call_id": tool.id, "content": tool_result})
                    break
                case "stop":
                    return


while True:
    run(messages)
    print(messages[-1]['content'])
    content = input(">> ")
    messages.append({"role": "user", "content": content})
    
