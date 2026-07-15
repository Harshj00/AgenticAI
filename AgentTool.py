from llm import chat
from memory import load_memory, save_memory
from prompts import SYSTEM_PROMPT
from parser import parse_tool_call
from calculator import calculator

class Agent:
    def run(self, user_input):
        
        memory = load_memory()
        messages = []
        messages.append(
            {"role": "system", 
             "content": SYSTEM_PROMPT
            }
        )

        messages.extend(memory)
        
        messages.append({"role": "user", "content": user_input})

        llm_response = chat(messages)

        tool_request = parse_tool_call(llm_response)

        if tool_request is None:
            memory.append({"role": "user", "content": user_input})
            memory.append({"role": "assistant", "content": llm_response})
            save_memory(memory)

            return llm_response
        
        print("Tool request")
        tool_result = ""
        if tool_request["tool"] == "calculator":
            expression = tool_request["expression"]
            tool_result = calculator(expression)
        
        else:
            tool_result = "Unknown tool requested."

        print("observation", tool_result)

        messages.append({"role": "assistant", "content": llm_response})

        messages.append({
                "role": "user",
                "content": f"tool result:\n{tool_result}\nNow answer the user's original question based on the tool result."
       })

        final_response = chat(messages)

        memory.append({"role": "user", "content": user_input})

        memory.append({"role": "assistant", "content": final_response})  
        save_memory(memory)

        return final_response