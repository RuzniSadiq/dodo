import argparse
import json
import sys
from pathlib import Path
from typing import Any

DB = Path.home() / ".dodo.json"

def load() -> list[dict[str, Any]]:
    return json.loads(DB.read_text()) if DB.exists() else []

def save(tasks: list[dict[str, Any]]) -> None:
    DB.write_text(json.dumps(tasks, indent=2))

def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="dodo")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("add").add_argument("text")
    sub.add_parser("list")
    sub.add_parser("done").add_argument("id", type=int)
    a = p.parse_args(argv)

    tasks = load()
    if a.cmd == "add":
        tasks.append({"id": len(tasks) + 1, "text": a.text, "done": False})
        save(tasks)
    elif a.cmd == "list":
        for t in tasks:
            print(f"{t['id']}. [{'x' if t['done'] else ' '}] {t['text']}")
    elif a.cmd == "done":
        for t in tasks:
            if t["id"] == a.id:
                t["done"] = True
        save(tasks)
    return 0

if __name__ == "__main__":
    sys.exit(main())