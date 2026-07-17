if __package__ in (None, ""):
    from calculator import calculator
    from time_tool import excecute as time_tool
    from weather import execute as weather
    from unit_converter import convert as unit_converter
    from web_search import execute as web_search
else:
    from .calculator import calculator
    from .time_tool import excecute as time_tool
    from .weather import execute as weather
    from .unit_converter import convert as unit_converter
    from .web_search import execute as web_search

TOOLS = {
    "calculator": calculator,
    "time": time_tool,
    "weather": weather,
    "unit_converter": unit_converter,
    "web_search": web_search,
}

def execute_tool(tool_name: str, argument: dict):
    tool = TOOLS.get(tool_name)

    if tool is None:
         return f"Unknown tool: {tool_name}"
    

    return tool(argument)

def list_tools():
    return list(TOOLS.keys())

if __name__ == "__main__":
    print("Registered tools:")
    print(
        execute_tool(
            "calculator",
            {
                "expression": "25*18"
            }
        )
    )
    print("\n")

    print(
        execute_tool(
            "time",
            {
                
            }
        )
    )