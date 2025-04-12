import json
from difflib import get_close_matches

DB_PATH = "database.json"

def load_database():
    try:
        with open(DB_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def save_to_database(question, answer):
    db = load_database()
    db[question] = answer
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)

def find_best_match(prompt):
    db = load_database()
    questions = list(db.keys())
    match = get_close_matches(prompt, questions, n=1, cutoff=0.7)
    if match:
        return db[match[0]]
    return None