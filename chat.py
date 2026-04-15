"""Zini AI chat interface (single-file assistant brain + modern Tkinter UI).

This file intentionally contains everything needed for chatting:
- conversation memory
- local knowledge retrieval
- friendly personality
- modern desktop interface (Tkinter, no heavy dependencies)
"""

from __future__ import annotations

import json
import random
import re
from datetime import datetime
from pathlib import Path
import difflib
import tkinter as tk
from tkinter import ttk


class ZiniAssistant:
    """Lightweight assistant engine used by the Tkinter UI."""

    def __init__(self, memory_file: str = "memory.json", knowledge_file: str = "data.txt") -> None:
        self.memory_path = Path(memory_file)
        self.knowledge_path = Path(knowledge_file)
        self.memory = self._load_memory()
        self.knowledge = self._load_knowledge()

        # Extra-friendly greetings (expanded set).
        self.greetings = [
            "Hey there! I'm Zini ✨",
            "Hi friend! Zini here, ready to help.",
            "Hello hello 👋 Let's build something awesome.",
            "Yo! Need answers, ideas, or a tiny joke?",
            "Welcome back! Your favorite tiny AI is online 😎",
            "Hi! I remembered my smile and my memory today.",
            "Hey! Ask me anything from your learned knowledge.",
            "Good to see you! Let's chat and learn together.",
        ]

        self.fallbacks = [
            "I don't know that yet, but I can learn if you teach me: teach topic: fact",
            "I'm still learning this one. Want to teach me quickly?",
            "Brain loading... teach me and I'll remember it forever (in data.txt 😄).",
        ]

        # Regex intent map.
        self.intent_patterns: list[tuple[str, re.Pattern[str]]] = [
            ("set_name", re.compile(r"(?:my name is|i am|i'm)\s+([a-zA-Z][a-zA-Z\-']{1,30})", re.IGNORECASE)),
            ("get_name", re.compile(r"(?:what is my name|do you remember my name)", re.IGNORECASE)),
            ("set_mood", re.compile(r"(?:i feel|i am feeling)\s+(.+)$", re.IGNORECASE)),
            ("time", re.compile(r"\b(?:time|clock)\b", re.IGNORECASE)),
            ("date", re.compile(r"\b(?:date|day today|today)\b", re.IGNORECASE)),
            ("learn_fact", re.compile(r"teach\s+(.+?)\s*[:=-]\s*(.+)$", re.IGNORECASE)),
            ("ask_fact", re.compile(r"(?:tell me about|what is|who is|explain|define)\s+(.+)$", re.IGNORECASE)),
            ("joke", re.compile(r"\b(?:joke|funny)\b", re.IGNORECASE)),
            ("thanks", re.compile(r"\b(?:thanks|thank you|thx)\b", re.IGNORECASE)),
            ("bye", re.compile(r"\b(?:bye|exit|quit|goodbye)\b", re.IGNORECASE)),
        ]

    def _load_memory(self) -> dict:
        if self.memory_path.exists():
            try:
                return json.loads(self.memory_path.read_text(encoding="utf-8"))
            except Exception:
                pass
        return {"facts": {}, "chat_log": []}

    def _save_memory(self) -> None:
        self.memory_path.write_text(json.dumps(self.memory, ensure_ascii=False, indent=2), encoding="utf-8")

    def _load_knowledge(self) -> dict[str, str]:
        knowledge: dict[str, str] = {}
        if not self.knowledge_path.exists():
            return knowledge
        with self.knowledge_path.open("r", encoding="utf-8") as file:
            for raw in file:
                line = raw.strip()
                if not line or "|" not in line:
                    continue
                topic, summary = line.split("|", 1)
                knowledge[topic.strip().lower()] = summary.strip()
        return knowledge

    def _append_knowledge(self, topic: str, summary: str) -> None:
        with self.knowledge_path.open("a", encoding="utf-8") as file:
            file.write(f"{topic.strip()}|{summary.strip()}\n")

    def _intent(self, user_text: str) -> tuple[str, str | None]:
        for intent, pattern in self.intent_patterns:
            match = pattern.search(user_text)
            if match:
                return intent, (match.group(1).strip() if match.groups() else None)
        return "unknown", None

    def _search_knowledge(self, query: str) -> tuple[str | None, str | None]:
        q = query.strip().lower()
        if q in self.knowledge:
            return q, self.knowledge[q]

        query_tokens = set(re.findall(r"[a-zA-Z0-9]+", q))
        best_topic = None
        best_score = 0
        for topic in self.knowledge:
            topic_tokens = set(re.findall(r"[a-zA-Z0-9]+", topic))
            score = len(query_tokens.intersection(topic_tokens))
            if score > best_score:
                best_score = score
                best_topic = topic
        if best_topic and best_score > 0:
            return best_topic, self.knowledge[best_topic]

        close = difflib.get_close_matches(q, list(self.knowledge.keys()), n=1, cutoff=0.72)
        if close:
            t = close[0]
            return t, self.knowledge[t]
        return None, None

    def respond(self, user_text: str) -> str:
        clean_text = user_text.strip().lower()
        intent, detail = self._intent(clean_text)

        if intent == "set_name" and detail:
            self.memory["name"] = detail.title()
            self._save_memory()
            return f"Nice to meet you, {self.memory['name']}! I'll remember that 💾"

        if intent == "get_name":
            name = self.memory.get("name")
            return f"Your name is {name} ✅" if name else "I don't know yet. Say: my name is ..."

        if intent == "set_mood" and detail:
            self.memory["mood"] = detail
            self._save_memory()
            return f"Thanks for sharing. I saved your mood: '{detail}'. I'm here for you 💛"

        if intent == "time":
            return f"Current UTC time: {datetime.utcnow().strftime('%H:%M:%S')} ⏰"

        if intent == "date":
            return f"Today is {datetime.utcnow().strftime('%A, %B %d, %Y')} (UTC) 📅"

        if intent == "learn_fact":
            learn_match = re.search(r"teach\s+(.+?)\s*[:=-]\s*(.+)$", user_text, re.IGNORECASE)
            if not learn_match:
                return "Format: teach topic: fact"
            topic = learn_match.group(1).strip().lower()
            fact = learn_match.group(2).strip()
            self.knowledge[topic] = fact
            self.memory.setdefault("facts", {})[topic] = fact
            self._append_knowledge(topic, fact)
            self._save_memory()
            return f"Learned ✅ Ask me later: tell me about {topic}"

        if intent == "ask_fact" and detail:
            found_topic, found_summary = self._search_knowledge(detail)
            if found_summary:
                return f"About {found_topic.title()}: {found_summary}"
            return random.choice(self.fallbacks)

        if intent == "joke":
            return random.choice([
                "I would tell a UDP joke, but you might not get it.",
                "Why did the coder stay calm? They had exception handling 😄",
                "I run on curiosity and tiny files.",
            ])

        if intent == "thanks":
            return random.choice([
                "Always happy to help 💙",
                "You're welcome! Keep the great questions coming.",
                "Anytime, friend 🚀",
            ])

        if intent == "bye":
            name = self.memory.get("name")
            return f"Bye {name}! Come back soon 👋" if name else "Bye! Come back soon 👋"

        # Unknown: try direct retrieval from entire message.
        found_topic, found_summary = self._search_knowledge(clean_text)
        if found_summary:
            return f"I found this: {found_summary}"

        name = self.memory.get("name")
        if name:
            return f"Hmm {name}, I'm still learning that. Use: teach topic: fact"
        return random.choice(self.fallbacks)


class ZiniChatUI:
    """Modern-feeling chat UI using Tkinter only (ships with Python)."""

    def __init__(self) -> None:
        self.assistant = ZiniAssistant()

        self.root = tk.Tk()
        self.root.title("Zini AI • Modern Chat")
        self.root.geometry("920x620")
        self.root.minsize(760, 520)

        # Dark modern palette.
        self.colors = {
            "bg": "#0f172a",
            "panel": "#111827",
            "user": "#1d4ed8",
            "zini": "#059669",
            "text": "#e5e7eb",
            "muted": "#94a3b8",
            "entry": "#1f2937",
        }
        self.root.configure(bg=self.colors["bg"])

        self._build_layout()
        self._post_system_message(random.choice(self.assistant.greetings))
        self._post_system_message("Tip: teach topic: fact  •  Ask: tell me about python  •  Type bye to close")

    def _build_layout(self) -> None:
        style = ttk.Style(self.root)
        style.theme_use("clam")

        container = tk.Frame(self.root, bg=self.colors["bg"])
        container.pack(fill="both", expand=True, padx=16, pady=16)

        header = tk.Frame(container, bg=self.colors["panel"], bd=0, highlightthickness=0)
        header.pack(fill="x", pady=(0, 10))

        title = tk.Label(
            header,
            text="🤖 Zini AI",
            bg=self.colors["panel"],
            fg=self.colors["text"],
            font=("Segoe UI", 18, "bold"),
            padx=16,
            pady=12,
        )
        title.pack(side="left")

        subtitle = tk.Label(
            header,
            text="friendly • helpful • lightweight",
            bg=self.colors["panel"],
            fg=self.colors["muted"],
            font=("Segoe UI", 10),
            padx=8,
        )
        subtitle.pack(side="left")

        chat_frame = tk.Frame(container, bg=self.colors["bg"])
        chat_frame.pack(fill="both", expand=True)

        self.chat_log = tk.Text(
            chat_frame,
            wrap="word",
            state="disabled",
            bg=self.colors["panel"],
            fg=self.colors["text"],
            insertbackground=self.colors["text"],
            relief="flat",
            bd=0,
            padx=14,
            pady=14,
            font=("Segoe UI", 11),
        )
        self.chat_log.pack(fill="both", expand=True)

        self.chat_log.tag_configure("zini", foreground="#a7f3d0")
        self.chat_log.tag_configure("user", foreground="#bfdbfe")
        self.chat_log.tag_configure("meta", foreground=self.colors["muted"], font=("Segoe UI", 9, "italic"))

        footer = tk.Frame(container, bg=self.colors["bg"])
        footer.pack(fill="x", pady=(10, 0))

        self.entry = tk.Entry(
            footer,
            bg=self.colors["entry"],
            fg=self.colors["text"],
            insertbackground=self.colors["text"],
            relief="flat",
            font=("Segoe UI", 11),
            bd=10,
        )
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.entry.bind("<Return>", lambda _event: self.send_message())

        send_btn = tk.Button(
            footer,
            text="Send",
            command=self.send_message,
            bg="#2563eb",
            fg="white",
            activebackground="#1e40af",
            activeforeground="white",
            relief="flat",
            padx=16,
            pady=10,
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
        )
        send_btn.pack(side="left")

        clear_btn = tk.Button(
            footer,
            text="Clear",
            command=self.clear_chat,
            bg="#334155",
            fg="white",
            activebackground="#1f2937",
            activeforeground="white",
            relief="flat",
            padx=12,
            pady=10,
            font=("Segoe UI", 10),
            cursor="hand2",
        )
        clear_btn.pack(side="left", padx=(8, 0))

    def _append_chat(self, speaker: str, message: str, tag: str) -> None:
        now = datetime.utcnow().strftime("%H:%M:%S UTC")
        self.chat_log.configure(state="normal")
        self.chat_log.insert("end", f"{speaker}: ", tag)
        self.chat_log.insert("end", f"{message}\n", tag)
        self.chat_log.insert("end", f"{now}\n\n", "meta")
        self.chat_log.configure(state="disabled")
        self.chat_log.see("end")

    def _post_system_message(self, text: str) -> None:
        self._append_chat("Zini", text, "zini")

    def clear_chat(self) -> None:
        self.chat_log.configure(state="normal")
        self.chat_log.delete("1.0", "end")
        self.chat_log.configure(state="disabled")
        self._post_system_message("Chat cleared ✅")

    def send_message(self) -> None:
        user_text = self.entry.get().strip()
        if not user_text:
            return
        self.entry.delete(0, "end")
        self._append_chat("You", user_text, "user")

        bot_reply = self.assistant.respond(user_text)
        self._append_chat("Zini", bot_reply, "zini")

        self.assistant.memory.setdefault("chat_log", []).append({"user": user_text, "zini": bot_reply})
        self.assistant.memory["chat_log"] = self.assistant.memory["chat_log"][-120:]
        self.assistant._save_memory()

        if re.search(r"\b(?:bye|exit|quit|goodbye)\b", user_text, re.IGNORECASE):
            self.root.after(800, self.root.destroy)

    def run(self) -> None:
        self.entry.focus_set()
        self.root.mainloop()


if __name__ == "__main__":
    ZiniChatUI().run()
