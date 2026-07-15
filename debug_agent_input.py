from llm import chat
from parser import parse_tool_call

msg = [{"role": "user", "content": "What is 25*18?"}]
resp = chat(msg)
print('llm raw:', repr(resp))
parsed = parse_tool_call(resp)
print('parsed:', parsed)
