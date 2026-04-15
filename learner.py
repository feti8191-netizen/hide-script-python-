"""Zini AI learner (upgraded).

Features:
- Generates a 1000-question learning bank automatically.
- Can auto-learn from Wikipedia summaries.
- Saves learned facts in data.txt (TOPIC|SUMMARY).
- Saves generated questions in questions_1000.txt.
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from urllib import error, parse, request


DATA_FILE = Path("data.txt")
QUESTIONS_FILE = Path("questions_1000.txt")

# High-value base topics; question bank expands from these.
BASE_TOPICS = [
    "Artificial intelligence", "Machine learning", "Deep learning", "Neural network", "Python (programming language)",
    "Algorithm", "Data structure", "Computer science", "Operating system", "Linux",
    "Windows", "Cybersecurity", "Encryption", "Hash function", "Computer network",
    "Internet", "World Wide Web", "Database", "SQL", "API",
    "HTTP", "JSON", "Git", "GitHub", "Cloud computing",
    "Virtual machine", "Docker (software)", "Natural language processing", "Computer vision", "Robotics",
    "Mathematics", "Algebra", "Calculus", "Statistics", "Probability",
    "Linear algebra", "Physics", "Chemistry", "Biology", "Astronomy",
    "Earth", "Solar System", "Milky Way", "Universe", "Climate change",
    "Electricity", "Renewable energy", "History", "Ancient Egypt", "Roman Empire",
    "Industrial Revolution", "World War I", "World War II", "United Nations", "Democracy",
    "Economics", "Inflation", "Supply and demand", "Blockchain", "Bitcoin",
    "Ethics", "Philosophy", "Psychology", "Memory", "Learning",
    "Creativity", "Communication", "Public speaking", "Project management", "Leadership",
    "Startup company", "Entrepreneurship", "Marketing", "Brand", "Customer service",
    "User interface", "User experience", "Mobile app", "Web development", "HTML",
    "CSS", "JavaScript", "Object-oriented programming", "Functional programming", "Test automation",
    "Software engineering", "Debugging", "Version control", "Open-source software", "Data privacy",
    "Computer security", "Ethical hacking", "Penetration test", "Risk management", "Decision-making",
    "Time management", "Productivity", "Critical thinking", "Problem solving", "Innovation",
]

QUESTION_TEMPLATES = [
    "What is {topic}?",
    "Explain {topic} in simple words.",
    "Why is {topic} important?",
    "How does {topic} work?",
    "Give a beginner example of {topic}.",
    "What are the main parts of {topic}?",
    "What are common mistakes in {topic}?",
    "When should someone learn {topic}?",
    "What skills connect to {topic}?",
    "What is the future of {topic}?",
]


def load_existing_topics() -> set[str]:
    existing: set[str] = set()
    if not DATA_FILE.exists():
        return existing
    with DATA_FILE.open("r", encoding="utf-8") as file:
        for raw_line in file:
            line = raw_line.strip()
            if not line or "|" not in line:
                continue
            topic, _summary = line.split("|", 1)
            existing.add(topic.strip().lower())
    return existing


def fetch_wikipedia_summary(topic: str) -> tuple[str | None, str | None]:
    encoded_topic = parse.quote(topic)
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{encoded_topic}"
    try:
        with request.urlopen(url, timeout=15) as response:
            payload = response.read().decode("utf-8")
            data = json.loads(payload)
            title = data.get("title", topic)
            summary = data.get("extract")
            if not summary:
                return None, None
            return title, summary.replace("\n", " ").strip()
    except error.HTTPError:
        return None, None
    except error.URLError:
        return None, None
    except Exception:
        return None, None


def save_topic(topic: str, summary: str) -> None:
    with DATA_FILE.open("a", encoding="utf-8") as file:
        file.write(f"{topic.strip()}|{summary.strip()}\n")


def build_question_bank(target_count: int = 1000) -> list[str]:
    """Create a 1000-question bank by combining templates with topics."""
    questions: list[str] = []

    # Start with template-combined questions.
    for topic in BASE_TOPICS:
        for template in QUESTION_TEMPLATES:
            questions.append(template.format(topic=topic))
            if len(questions) >= target_count:
                return questions

    # If still short, add topic-focused variants.
    suffixes = [
        "for students",
        "for developers",
        "in real life",
        "for beginners",
        "in history",
        "in business",
        "in science",
        "in modern technology",
    ]

    idx = 0
    while len(questions) < target_count:
        topic = BASE_TOPICS[idx % len(BASE_TOPICS)]
        suffix = suffixes[idx % len(suffixes)]
        questions.append(f"How is {topic} used {suffix}?")
        idx += 1

    return questions


def save_question_bank(questions: list[str]) -> None:
    with QUESTIONS_FILE.open("w", encoding="utf-8") as file:
        for q in questions:
            file.write(f"{q}\n")


def auto_learn_from_topics(topics: list[str], delay_seconds: float = 0.7, max_count: int = 1000) -> None:
    known_topics = load_existing_topics()
    learned_count = 0
    skipped_count = 0

    print(f"🚀 Auto-learning up to {max_count} topics...")
    for index, topic in enumerate(topics, start=1):
        if learned_count >= max_count:
            break

        print(f"[{index}/{len(topics)}] Learning: {topic}")
        normalized = topic.strip().lower()
        if normalized in known_topics:
            print("   ↳ Skipped (already exists)")
            skipped_count += 1
            continue

        title, summary = fetch_wikipedia_summary(topic)
        if not title or not summary:
            print("   ↳ Could not fetch right now")
            continue

        save_topic(title, summary)
        known_topics.add(title.strip().lower())
        learned_count += 1
        print(f"   ↳ Learned: {title}")
        time.sleep(delay_seconds)

    print("\n✅ Auto-learning finished")
    print(f"Learned this run: {learned_count}")
    print(f"Skipped existing: {skipped_count}")
    print(f"Knowledge file: {DATA_FILE.resolve()}")


def manual_learn_loop() -> None:
    known_topics = load_existing_topics()
    print("Type a topic and I will learn it from Wikipedia. Type 'quit' to stop.")
    while True:
        topic = input("Topic: ").strip()
        if topic.lower() in {"quit", "exit", "bye"}:
            break
        if not topic:
            continue
        if topic.lower() in known_topics:
            print("Already learned this topic.")
            continue

        title, summary = fetch_wikipedia_summary(topic)
        if not title or not summary:
            print("Could not learn this topic right now.")
            continue

        save_topic(title, summary)
        known_topics.add(title.strip().lower())
        print(f"✅ Learned: {title}")


def main() -> None:
    questions = build_question_bank(1000)
    save_question_bank(questions)

    print("\n=== Zini AI Learner (Upgraded) ===")
    print("1) Build/refresh 1000 question list only")
    print("2) Auto-learn from base topics now")
    print("3) Manual learning (topic by topic)")

    choice = input("Choose 1, 2, or 3: ").strip()
    if choice == "1":
        print(f"✅ Generated {len(questions)} questions in {QUESTIONS_FILE}")
    elif choice == "2":
        # Use unique base topics as learning source.
        unique_topics = sorted(set(BASE_TOPICS))
        auto_learn_from_topics(unique_topics, delay_seconds=0.7, max_count=1000)
        print(f"✅ Generated {len(questions)} questions in {QUESTIONS_FILE}")
    else:
        manual_learn_loop()
        print(f"✅ Question list available in {QUESTIONS_FILE}")


if __name__ == "__main__":
    main()
