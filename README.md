# Zini AI (Upgraded, Lightweight)

Zini AI now runs with **two files only**:
- `chat.py` → full assistant brain + modern desktop chat interface (Tkinter)
- `learner.py` → upgraded learner + auto-generated 1000-question learning list

No heavy ML libraries are used.

## Quick Start

```bash
python learner.py
python chat.py
```

## What changed

- Removed `zini_ai.py` (logic moved directly into `chat.py`).
- Added a modern dark chat interface in `chat.py` with:
  - message area with timestamps,
  - friendly personality responses,
  - expanded greetings,
  - quick input + send/clear buttons.
- Upgraded `learner.py` with:
  - automatic **1000-question list** saved to `questions_1000.txt`,
  - Wikipedia learning mode that stores facts in `data.txt`,
  - manual topic-learning mode.

## Data files

- `data.txt` → long-term learned facts in `TOPIC|SUMMARY` format.
- `memory.json` → conversation memory (name, mood, chat log).
- `questions_1000.txt` → generated learning question bank.

## Example teach command

In chat, type:

```text
teach python: Python is a high-level programming language.
```

Then ask:

```text
tell me about python
```
