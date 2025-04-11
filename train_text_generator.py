
import torch
import torch.nn as nn

class SimpleTokenizer:
    def __init__(self, texts):
        vocab = sorted(set("".join(texts)))
        self.char2idx = {ch: idx + 1 for idx, ch in enumerate(vocab)}
        self.char2idx["<pad>"] = 0
        self.idx2char = {idx: ch for ch, idx in self.char2idx.items()}

    def encode(self, text):
        return [self.char2idx.get(ch, 0) for ch in text]

    def decode(self, ids):
        return "".join(self.idx2char.get(i, "") for i in ids)

    def vocab_size(self):
        return len(self.char2idx)

class TextGenerator(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_dim, num_layers=1):
        super(TextGenerator, self).__init__()
        self.embed = nn.Embedding(vocab_size, embedding_dim)
        self.lstm = nn.LSTM(embedding_dim, hidden_dim, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_dim, vocab_size)

    def forward(self, x, hidden=None):
        x = self.embed(x)
        out, hidden = self.lstm(x, hidden)
        out = self.fc(out)
        return out, hidden

def train_model():
    texts = ["hello world", "hi there", "how are you"]
    tokenizer = SimpleTokenizer(texts)
    encoded = [tokenizer.encode(t) for t in texts]
    padded = [seq + [0] * (12 - len(seq)) for seq in encoded]
    data = torch.tensor(padded)

    vocab_size = tokenizer.vocab_size()
    model = TextGenerator(vocab_size, 128, 256)

    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.005)

    for epoch in range(5):
        for i in range(len(data)):
            x = data[i:i+1, :-1]
            y = data[i:i+1, 1:]
            optimizer.zero_grad()
            out, _ = model(x)
            loss = criterion(out.view(-1, vocab_size), y.view(-1))
            loss.backward()
            optimizer.step()
        print(f"Epoch {epoch+1}, Loss: {loss.item():.4f}")

    torch.save(model.state_dict(), "text_generator.pth")
    print("Модель сохранена в text_generator.pth")

if __name__ == "__main__":
    train_model()
