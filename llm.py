"""
Lightweight local LLM emulator to avoid external dependencies.

Behavior:
- If the latest user message asks for time/date, returns current India time.
- If the latest user message appears to require calculation, returns a JSON
  string with the calculator tool request (matching prompts.py expectations).
- Otherwise returns a simple assistant reply.

This keeps the app runnable without external LLM packages.
"""
import json
import re
from datetime import datetime


def _looks_like_calculation(text: str) -> bool:
    if not text:
        return False
    return bool(re.search(r"\d", text)) or bool(re.search(r"\bsqrt\b|\babs\b|\blog\b|\blog10\b|\bsin\b|\bcos\b|\btan\b|\bexp\b|\bfactorial\b|\bpi\b", text, re.IGNORECASE))


def _extract_expression(text: str) -> str:
    # Try to extract contiguous math-like token groups and pick the one
    # containing digits (to avoid matching whitespace-only groups).
    matches = re.findall(r"[0-9\.\+\-\*\/\%\(\)\s]+", text)
    for m in matches:
        if re.search(r"\d", m):
            return m.strip()
    # fallback: try to extract a compact expression (digits and operators)
    m2 = re.search(r"[0-9\.+\-\*/%()]+", text)
    if m2:
        return m2.group(0).strip()
    # fallback: return the original text
    return text.strip()


def _looks_like_unit_conversion(text: str) -> bool:
    if not text:
        return False
    return bool(re.search(r"\bconvert\b|\bin\b|\bto\b|\binto\b", text, re.IGNORECASE) and re.search(r"\d", text))


def _extract_conversion(text: str):
    match = re.search(
        r"(?P<value>-?[0-9]+(?:\.[0-9]+)?)\s*(?P<from>[A-Za-z°/\s]+)\s*(?:to|in|into)\s*(?P<to>[A-Za-z°/\s]+)",
        text,
        re.IGNORECASE,
    )
    if not match:
        return None
    value = match.group('value').strip()
    from_unit = match.group('from').strip()
    to_unit = match.group('to').strip()
    return value, from_unit, to_unit


def _looks_like_weather(text: str) -> bool:
    if not text:
        return False
    return bool(re.search(r"\bweather\b|\bforecast\b|\btemperature\b|\bclimate\b", text, re.IGNORECASE))


def _extract_city(text: str):
    match = re.search(r"(?:weather|forecast|temperature|climate)(?:\s+for|\s+in|\s+at)?\s+([A-Za-z][A-Za-z\s'\-]+)", text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return None


def chat(messages):
    """Accepts the same message formats used in the project (list of dicts or
    list-like objects). Returns a string response. For calculator requests the
    returned string is JSON (so `parser.parse_tool_call` can load it).
    """
    content = ""
    if isinstance(messages, (list, tuple)) and messages:
        last = messages[-1]
        if isinstance(last, dict):
            content = last.get("content", "")
        else:
            content = getattr(last, "content", str(last))
    else:
        content = str(messages)

    text = content or ""

    # If the message is the agent's follow-up carrying tools_result, produce a
    # natural final answer instead of another calculator call.
    if text.strip().lower().startswith("tools_result"):
        m = re.search(r"tools_result:\s*\n(.*?)\nNow answer", text, re.S | re.IGNORECASE)
        if m:
            result = m.group(1).strip()
        else:
            parts = text.split(':', 1)
            result = parts[1].strip() if len(parts) > 1 else text
        return f"Answer based on tools result: {result}"

    # Name query handler
    if re.search(r"\bwhat(?:'s| is) my name\b|\bwho am i\b|\bremember my name\b", text, re.IGNORECASE):
        return "I don't have your name yet. Tell me your name and I will remember it."

    # Time/date request handler
    if re.search(r"\btime\b|\bdate\b|current time|current date", text, re.IGNORECASE):
        return json.dumps({"tool": "time"})

    # Weather handler
    if _looks_like_weather(text):
        city = _extract_city(text)
        tool_req = {"tool": "weather", "city": city or "Delhi"}
        return json.dumps(tool_req)

    # Web search handler
    if re.search(r"\bsearch\b|\bfind\b|\blook up\b|\bweb search\b|\bgoogle\b", text, re.IGNORECASE):
        query = text.strip()
        tool_req = {"tool": "web_search", "query": query}
        return json.dumps(tool_req)

    # Unit conversion handler: return JSON for unit_converter tool
    if _looks_like_unit_conversion(text):
        conversion = _extract_conversion(text)
        if conversion:
            quantity, from_unit, to_unit = conversion
            tool_req = {
                "tool": "unit_converter",
                "quantity": quantity,
                "from_unit": from_unit,
                "to_unit": to_unit,
            }
            return json.dumps(tool_req)

    # Calculation handler: return JSON matching prompts.py expected format
    if _looks_like_calculation(text):
        expr = _extract_expression(text)
        tool_req = {"tool": "calculator", "expression": expr}
        return json.dumps(tool_req)

    # Default reply
    return "I am a local assistant. Ask me to calculate something or a simple question."


if __name__ == "__main__":
    msgs = [{"role": "user", "content": "What is 25*18?"}]
    print(chat(msgs))
