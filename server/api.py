
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import torch
import torchvision.transforms as transforms
from PIL import Image
import io

from models.classifier import ClassifierRegressor
from models.generator import TextGenerator
from models.image_model import CNNClassifier

app = FastAPI()

# Загрузка моделей
classifier_model = ClassifierRegressor(input_size=10, hidden_size=64, num_classes=2, regression=False)
classifier_model.load_state_dict(torch.load("classifier.pth"))
classifier_model.eval()

generator_model = TextGenerator(vocab_size=100, embedding_dim=32, hidden_dim=64)
generator_model.load_state_dict(torch.load("text_generator.pth"))
generator_model.eval()

cnn_model = CNNClassifier(num_classes=2)
cnn_model.load_state_dict(torch.load("cnn.pth"))
cnn_model.eval()

# Эндпоинт для классификации изображения
@app.post("/classify-image")
async def classify_image(file: UploadFile = File(...)):
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    transform = transforms.Compose([
        transforms.Resize((32, 32)),
        transforms.ToTensor()
    ])
    input_tensor = transform(image).unsqueeze(0)
    with torch.no_grad():
        output = cnn_model(input_tensor)
        pred = output.argmax(dim=1).item()
    return {"prediction": pred}

# Эндпоинт для генерации текста (заглушка)
class TextInput(BaseModel):
    prompt: str

@app.post("/generate-text")
async def generate_text(data: TextInput):
    prompt = data.prompt
    # Заглушка генерации (так как реального токенизатора и словаря нет)
    generated = prompt + " ...generated text..."
    return {"generated_text": generated}

# Эндпоинт для классификации по вектору признаков
@app.post("/classify-vector")
async def classify_vector(data: list[float]):
    tensor = torch.tensor([data])
    with torch.no_grad():
        output = classifier_model(tensor)
        pred = output.argmax(dim=1).item()
    return {"prediction": pred}
