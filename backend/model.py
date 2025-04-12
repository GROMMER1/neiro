from sentence_transformers import SentenceTransformer, util

class NeuralResponder:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.knowledge = self.load_knowledge()

    def load_knowledge(self):
        try:
            with open("backend/knowledge/data.txt", "r", encoding="utf-8") as f:
                return [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            return []

    def generate_response(self, query):
        if not self.knowledge:
            return "Я пока ничего не знаю, обучите меня!"
        query_emb = self.model.encode(query, convert_to_tensor=True)
        knowledge_embs = self.model.encode(self.knowledge, convert_to_tensor=True)
        hits = util.semantic_search(query_emb, knowledge_embs, top_k=1)
        best_match = self.knowledge[hits[0][0]["corpus_id"]]
        return best_match

def load_neural_responder_lazy():
    return NeuralResponder()