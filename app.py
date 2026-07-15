from agent import Agent
def main():
    print("=" * 60)
    print("AI AGENT")
    print("=" * 60)
    print("type 'exit' to quit.")
    print()


    agent = Agent()
    while True:
        user_input = input("You: ").strip()

        if not user_input:
            continue

        if user_input.lower() in ["exit", "quit"]:
            break

        try:
            response = agent.run(user_input)
            print(f"Agent: {response}\n")
        
        except Exception as e:
            print(f"Error: {e}\n")

if __name__ == "__main__":
    main()