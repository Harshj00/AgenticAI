from llm import chat
import json
resp = chat([{"role":"user","content":"What is 25*18?"}])
print('raw:', resp)
try:
    print('parsed:', json.loads(resp))
except Exception as e:
    print('json error:', e)
