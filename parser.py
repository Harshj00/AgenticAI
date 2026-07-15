import json 

def parse_tool_call(response):
    try: 
        tool_request = json.loads(response)
        if(
            isinstance(tool_request, dict) and
            "tool" in tool_request
        ):
            return tool_request
    except Exception:
        pass

    return None

if __name__ == "__main__":
    # response = """
    # {
    # "tool": "calculator",
    # "expression": "25**2"
    # }"""

    response = "Hello, how are you?"
    
    result = parse_tool_call(response)
    print(result)