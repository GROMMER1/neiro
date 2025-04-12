from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments, DataCollatorForLanguageModeling
from datasets import Dataset
import torch
import json
import glob
from langdetect import detect

MODEL_NAME = "microsoft/DialoGPT-small"
OUTPUT_DIR = "./backend/training/fine_tuned_multilang"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

# Загружаем JSON или TXT-файлы как обучающую выборку
def load_data():
    texts = []

    # JSON диалоги
    for file in glob.glob("./backend/training/data/*.json"):
        with open(file, encoding="utf-8") as f:
            records = json.load(f)
            for entry in records:
                text = entry.get("text")
                if text:
                    texts.append(text)

    # TXT файлы (многоязычные)
    for file in glob.glob("./backend/training/data/*.txt"):
        with open(file, encoding="utf-8") as f:
            lines = f.readlines()
            texts.extend([line.strip() for line in lines if line.strip()])

    return Dataset.from_dict({"text": texts})

def tokenize_function(example):
    return tokenizer(example["text"], truncation=True, padding=True, max_length=512)

dataset = load_data()
tokenized_dataset = dataset.map(tokenize_function, batched=True)

training_args = TrainingArguments(
    output_dir=OUTPUT_DIR,
    overwrite_output_dir=True,
    num_train_epochs=4,
    per_device_train_batch_size=4,
    save_steps=500,
    save_total_limit=2,
    logging_dir="./backend/training/logs",
    logging_steps=100,
    fp16=torch.cuda.is_available(),
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    tokenizer=tokenizer,
    data_collator=data_collator,
)

trainer.train()
model.save_pretrained(OUTPUT_DIR)
tokenizer.save_pretrained(OUTPUT_DIR)