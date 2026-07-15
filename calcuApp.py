from AgentTool import Agent

def main():
    print("Welcome to the AI Agent!")
    print("Type 'exit' to quit.")

    agent = Agent()

    while True:
        user_input = input("You: ").strip()

        if not user_input:
            continue

        if user_input.lower() == "exit":
            break

        try:
            response = agent.run(user_input)
            print("Agent:", response)

        except Exception as e:
            print("Error:", str(e))

if __name__ == "__main__":
    main()