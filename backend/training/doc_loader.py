import os
import json
import docx
import glob
from PyPDF2 import PdfReader

def extract_from_pdf(path):
    try:
        reader = PdfReader(path)
        return "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    except Exception as e:
        return f"Ошибка чтения PDF: {e}"

def extract_from_docx(path):
    try:
        doc = docx.Document(path)
        return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
    except Exception as e:
        return f"Ошибка чтения DOCX: {e}"

def collect_documents(input_dir="backend/training/documents", output_file="backend/training/data/compiled_docs.txt"):
    os.makedirs("backend/training/data", exist_ok=True)
    texts = []

    for file in glob.glob(os.path.join(input_dir, "*")):
        if file.endswith(".pdf"):
            texts.append(extract_from_pdf(file))
        elif file.endswith(".docx"):
            texts.append(extract_from_docx(file))

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n\n".join(texts))

    print(f"[✓] Сохранено {len(texts)} документов в {output_file}")