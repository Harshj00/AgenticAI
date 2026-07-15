import os
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MEMORY_FILE = BASE_DIR / "memory.json"


def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return []

    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception:
        return []


def save_memory(memory):
    with open(MEMORY_FILE, "w", encoding="utf-8") as file:
        json.dump(memory, file, ensure_ascii=False, indent=4)


def add_message(memory, role, content):
    memory.append({
        "role": role,
        "content": content
    })
    return memory


if __name__ == "__main__":
    print("Loading memory...")
    memory = load_memory()

    print(memory)

    print("\nAdding Message to memory...")

    add_message(memory, "user", "Hello, how are you?")
    add_message(memory, "assistant", "I'm doing well, thank you!")

    save_memory(memory)

    print(load_memory())