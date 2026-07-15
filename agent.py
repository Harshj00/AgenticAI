from llm import chat
from memory import load_memory, save_memory
from prompts import SYSTEM_PROMPT
from parser import parse_tool_call
from tools import calculator, unit_converter

class Agent:

    def run(self, user_input: str) -> str:
        memory = load_memory()

        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },]
        messages.extend(memory)
        messages.append(
            {
                "role": "user",
                "content": user_input
            })
        
        llm_response = chat(messages)
        tools_request = parse_tool_call(llm_response)

        if tools_request is None:
            memory.append({"role": "user", "content": user_input})
            
            memory.append({"role": "assistant", "content": llm_response})
            save_memory(memory)
            return llm_response
        
        print("Tools requested:")
        tools_result =""
        if tools_request['tool'] == 'calculator':
            expression = tools_request['expression']
            tools_result = calculator(expression)
        elif tools_request['tool'] == 'unit_converter':
            tools_result = unit_converter(tools_request)
        else:
            tools_result = f"Tool is not supported."


        print("Observation: ", tools_result)

        messages.append({
            "role": "assistant",
            "content": llm_response
        })
        messages.append({
            "role": "user",
            "content": f"tools_result: \n{tools_result}\nNow answer the original question based on the tools result."  
        })

        final_response = chat(messages)
        memory.append({"role": "user", "content": user_input})
        memory.append({"role": "assistant", "content": final_response})

        save_memory(memory)
        
        return final_response