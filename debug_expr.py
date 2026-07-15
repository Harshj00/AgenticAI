from llm import _extract_expression, _looks_like_calculation
text = 'What is 25*18?'
print('text repr:', repr(text))
print('chars:', [ord(c) for c in text])
print('looks_like:', _looks_like_calculation(text))
import re
m = re.search(r"[0-9\.\+\-\*\/\%\(\)\s]+", text)
print('raw re match:', m)
print('re group0:', repr(m.group(0)) if m else None)
print('extracted:', repr(_extract_expression(text)))
