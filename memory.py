import os
import json
import errno
from pathlib import Path

# Strategy:
# 1) Prefer an explicit path from env `MEMORY_FILE_PATH`.
# 2) Use project-local memory.json during local dev.
# 3) If filesystem is read-only (serverless), fall back to `/tmp/memory.json`.
# 4) If writing still fails, keep an in-memory cache for the lifetime of the process.

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_MEMORY_FILE = BASE_DIR / "memory.json"
MEMORY_FILE = Path(os.getenv("MEMORY_FILE_PATH", str(DEFAULT_MEMORY_FILE)))

# In-memory fallback
_in_memory_cache = None

def _is_writable(path: Path) -> bool:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        # try opening for append/create
        with open(path, "a", encoding="utf-8"):
            pass
        return True
    except OSError:
        return False

# Choose a usable memory file at import time
if not _is_writable(MEMORY_FILE):
    tmp_path = Path("/tmp") / "memory.json"
    if _is_writable(tmp_path):
        MEMORY_FILE = tmp_path
    else:
        # final fallback: use in-memory only
        _in_memory_cache = []


def load_memory():
    global _in_memory_cache
    if _in_memory_cache is not None:
        return list(_in_memory_cache)

    try:
        if not MEMORY_FILE.exists():
            return []
        with open(MEMORY_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception:
        # if anything goes wrong, return empty history
        return []


def save_memory(memory):
    global MEMORY_FILE, _in_memory_cache
    if _in_memory_cache is not None:
        # store only in memory (no persistent storage available)
        _in_memory_cache = list(memory)
        return

    try:
        with open(MEMORY_FILE, "w", encoding="utf-8") as file:
            json.dump(memory, file, ensure_ascii=False, indent=4)
    except OSError as e:
        # If filesystem is read-only, try /tmp as a fallback
        if e.errno in (errno.EROFS, errno.EACCES, errno.EROFS if hasattr(errno, 'EROFS') else None):
            try:
                alt = Path("/tmp") / "memory.json"
                alt.parent.mkdir(parents=True, exist_ok=True)
                with open(alt, "w", encoding="utf-8") as file:
                    json.dump(memory, file, ensure_ascii=False, indent=4)
                MEMORY_FILE = alt
                return
            except Exception:
                # finally fall back to in-memory cache
                _in_memory_cache = list(memory)
                return
        else:
            # other OS errors -> use in-memory fallback
            _in_memory_cache = list(memory)
            return


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