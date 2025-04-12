
import json
import os

KNOWLEDGE_FILE = "knowledge_base.json"

def load_knowledge():
    if not os.path.exists(KNOWLEDGE_FILE):
        return []
    with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_knowledge(data):
    with open(KNOWLEDGE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_fact(prompt, response):
    knowledge = load_knowledge()
    knowledge.append({"prompt": prompt, "response": response})
    save_knowledge(knowledge)

def search_knowledge(query):
    knowledge = load_knowledge()
    results = []
    for item in knowledge:
        if query.lower() in item["prompt"].lower():
            results.append(item["response"])
    return results
