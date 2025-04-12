import time
import os
import subprocess

WATCH_DIR = "./backend/training/documents"
LOADED_FLAG = "./backend/training/.last_loaded"

def get_latest_state():
    files = os.listdir(WATCH_DIR)
    timestamps = [os.path.getmtime(os.path.join(WATCH_DIR, f)) for f in files]
    return max(timestamps) if timestamps else 0

def already_loaded(latest_time):
    if os.path.exists(LOADED_FLAG):
        with open(LOADED_FLAG, "r") as f:
            saved = float(f.read().strip())
            return saved == latest_time
    return False

def save_loaded_time(t):
    with open(LOADED_FLAG, "w") as f:
        f.write(str(t))

def main():
    print("👀 Watching for new training documents...")
    while True:
        latest = get_latest_state()
        if not already_loaded(latest):
            print("📄 New documents detected. Starting loader + training...")
            subprocess.run(["python", "backend/training/doc_loader.py"])
            subprocess.run(["python", "backend/training/train_multilang.py"])
            save_loaded_time(latest)
            print("✅ Training complete. Watching again...")
        time.sleep(60)

if __name__ == "__main__":
    main()