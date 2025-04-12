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
