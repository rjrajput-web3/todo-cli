# todo-cli

A tiny file-based todo list in one Python file. No dependencies, no server, no account.

## What it does

- Add tasks, list them, mark one done, and clear completed tasks.
- Tasks are stored in `todo.json` next to the script. Nothing leaves your machine.
- A corrupt `todo.json` is never silently overwritten — the tool stops and tells you.

## How to run

Requires Python 3.8+.

```sh
python todo.py add "Buy milk"
python todo.py list
python todo.py done 1
python todo.py clear-done
```

## Example output

```text
$ python todo.py add "Buy milk"
Added #1: Buy milk
$ python todo.py list
1. [ ] Buy milk
$ python todo.py done 1
Done: Buy milk
$ python todo.py list
1. [x] Buy milk
```

## Exit codes

- `0` — success
- `2` — usage error, bad task number, or an unreadable `todo.json`
