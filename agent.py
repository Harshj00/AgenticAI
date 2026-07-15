import re

from llm import chat
from memory import load_memory, save_memory
from prompts import SYSTEM_PROMPT
from parser import parse_tool_call
from tools.registry import execute_tool


class Agent:
    def __init__(self):
        self.session_name = None

    def _remember_name(self, user_input: str):
        if not user_input:
            return None

        name_patterns = [
            r"\bmy name is\s+([A-Za-z][A-Za-z .'-]+)",
            r"\bi am\s+([A-Za-z][A-Za-z .'-]+)",
            r"\bcall me\s+([A-Za-z][A-Za-z .'-]+)",
        ]

        for pattern in name_patterns:
            match = re.search(pattern, user_input, re.IGNORECASE)
            if match:
                name = match.group(1).strip()
                if name.lower() not in {"a", "an", "the"}:
                    self.session_name = name
                    return name

        return None

    def _is_name_query(self, user_input: str) -> bool:
        return bool(re.search(r"\b(what(?:'s| is) my name|who am i|do you remember my name|remember my name)\b", user_input, re.IGNORECASE))

    def _is_name_assignment(self, user_input: str) -> bool:
        return bool(re.search(r"\b(my name is|i am|call me)\b", user_input, re.IGNORECASE))

    def _is_greeting(self, user_input: str) -> bool:
        return bool(re.search(r"\b(hi|hello|hey|yo|yoo)\b", user_input, re.IGNORECASE))

    def run(self, user_input: str) -> str:
        memory = load_memory()
        self._remember_name(user_input)

        # restore name from conversation history if the session has no local name
        if not self.session_name:
            for item in memory:
                if item.get("role") in {"user", "assistant"}:
                    self._remember_name(item.get("content", ""))

        if self._is_name_query(user_input) and self.session_name:
            return f"Your name is {self.session_name}."

        if self._is_name_assignment(user_input) and self.session_name:
            return f"Nice to meet you, {self.session_name}."

        if self._is_greeting(user_input) and self.session_name:
            return f"Hello {self.session_name}! What can I help you with today?"

        system_prompt = SYSTEM_PROMPT
        if self.session_name:
            system_prompt += f"\nThe user's name is {self.session_name}. Use it naturally in replies when appropriate."

        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(memory)
        messages.append({"role": "user", "content": user_input})

        llm_response = chat(messages)
        tools_request = parse_tool_call(llm_response)

        if tools_request is None:
            memory.append({"role": "user", "content": user_input})
            memory.append({"role": "assistant", "content": llm_response})
            save_memory(memory)
            return llm_response

        print("Tools requested:")
        try:
            tools_result = execute_tool(tools_request["tool"], tools_request)
        except Exception as exc:
            tools_result = f"Tool error: {exc}"

        print("Observation: ", tools_result)

        messages.append({"role": "assistant", "content": llm_response})
        messages.append({
            "role": "user",
            "content": f"tools_result: \n{tools_result}\nNow answer the original question based on the tools result."
        })

        final_response = chat(messages)
        memory.append({"role": "user", "content": user_input})
        memory.append({"role": "assistant", "content": final_response})

        save_memory(memory)
        return final_response