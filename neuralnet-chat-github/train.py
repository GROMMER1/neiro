
import torch
import numpy as np

from models.classifier import ClassifierRegressor
from models.generator import TextGenerator
from models.image_model import CNNClassifier
from utils.tokenizer import SimpleTokenizer

from torch.utils.data import DataLoader, TensorDataset
from torch import nn, optim


def train_classifier():
    print("Обучение классификатора...")
    X = np.random.rand(500, 10).astype(np.float32)
    y = np.random.randint(0, 2, 500)

    model = ClassifierRegressor(10, 64, 2)
    criterion = nn.NLLLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    X_tensor = torch.tensor(X)
    y_tensor = torch.tensor(y)
    dataset = TensorDataset(X_tensor, y_tensor)
    dataloader = DataLoader(dataset, batch_size=32, shuffle=True)

    for epoch in range(5):
        for batch_X, batch_y in dataloader:
            optimizer.zero_grad()
            output = model(batch_X)
            loss = criterion(output, batch_y)
            loss.backward()
            optimizer.step()
    torch.save(model.state_dict(), "classifier.pth")


def train_generator():
    print("Обучение генератора текста...")
    vocab_size = 100
    model = TextGenerator(vocab_size, embedding_dim=32, hidden_dim=64)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    data = torch.randint(0, vocab_size, (500, 10))
    targets = torch.randint(0, vocab_size, (500, 10))

    dataset = TensorDataset(data, targets)
    dataloader = DataLoader(dataset, batch_size=32, shuffle=True)

    for epoch in range(3):
        for batch_X, batch_y in dataloader:
            optimizer.zero_grad()
            output, _ = model(batch_X)
            loss = criterion(output.view(-1, vocab_size), batch_y.view(-1))
            loss.backward()
            optimizer.step()
    torch.save(model.state_dict(), "text_generator.pth")


def train_cnn():
    print("Обучение CNN классификатора...")
    model = CNNClassifier(num_classes=2)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    images = torch.randn(100, 3, 32, 32)
    labels = torch.randint(0, 2, (100,))

    dataset = TensorDataset(images, labels)
    dataloader = DataLoader(dataset, batch_size=16, shuffle=True)

    for epoch in range(3):
        for batch_X, batch_y in dataloader:
            optimizer.zero_grad()
            output = model(batch_X)
            loss = criterion(output, batch_y)
            loss.backward()
            optimizer.step()
    torch.save(model.state_dict(), "cnn.pth")


if __name__ == "__main__":
    train_classifier()
    train_generator()
    train_cnn()
