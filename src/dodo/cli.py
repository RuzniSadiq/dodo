import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any


def db_path() -> Path:
    """Task file: $DODO_FILE if set, else ~/.dodo.json. Resolved per call."""
    override = os.environ.get("DODO_FILE")
    return Path(override) if override else Path.home() / ".dodo.json"

def load() -> list[dict[str, Any]]:
    db = db_path()
    return json.loads(db.read_text()) if db.exists() else []

def save(tasks: list[dict[str, Any]]) -> None:
    db_path().write_text(json.dumps(tasks, indent=2))

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