#!/usr/bin/env python3
"""todo-cli: a tiny file-based todo list. No dependencies, no server.

Usage:
    python todo.py add "Buy milk"
    python todo.py list
    python todo.py done 2
    python todo.py clear-done

Tasks live in todo.json next to this script. Nothing leaves your machine.
"""

import json
import sys
from pathlib import Path

DB = Path(__file__).with_name("todo.json")


def load():
    if not DB.exists():
        return []
    try:
        data = json.loads(DB.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        print("todo.json is not valid JSON; refusing to overwrite it.", file=sys.stderr)
        return None
    return data if isinstance(data, list) else []


def save(tasks):
    DB.write_text(json.dumps(tasks, indent=2), encoding="utf-8")


def cmd_add(args):
    if not args:
        print('Usage: python todo.py add "task text"', file=sys.stderr)
        return 2
    tasks = load()
    if tasks is None:
        return 2
    tasks.append({"text": " ".join(args), "done": False})
    save(tasks)
    print(f"Added #{len(tasks)}: {' '.join(args)}")
    return 0


def cmd_list(_args=None):
    tasks = load()
    if tasks is None:
        return 2
    if not tasks:
        print("Nothing to do. Add one with: python todo.py add \"task\"")
        return 0
    for i, task in enumerate(tasks, 1):
        mark = "[x]" if task.get("done") else "[ ]"
        print(f"{i}. {mark} {task.get('text', '')}")
    return 0


def cmd_done(args):
    tasks = load()
    if tasks is None:
        return 2
    if len(args) != 1 or not args[0].isdigit():
        print("Usage: python todo.py done <number>", file=sys.stderr)
        return 2
    index = int(args[0]) - 1
    if not 0 <= index < len(tasks):
        print("No task with that number.", file=sys.stderr)
        return 2
    tasks[index]["done"] = True
    save(tasks)
    print(f"Done: {tasks[index]['text']}")
    return 0


def cmd_clear_done(_args=None):
    tasks = load()
    if tasks is None:
        return 2
    remaining = [t for t in tasks if not t.get("done")]
    removed = len(tasks) - len(remaining)
    save(remaining)
    print(f"Cleared {removed} completed task(s).")
    return 0


COMMANDS = {"add": cmd_add, "list": cmd_list, "done": cmd_done, "clear-done": cmd_clear_done}


def main(argv):
    if len(argv) < 2 or argv[1] not in COMMANDS:
        print("Usage: python todo.py {add|list|done|clear-done} [args]", file=sys.stderr)
        return 2
    handler = COMMANDS[argv[1]]
    return handler(argv[2:])


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
