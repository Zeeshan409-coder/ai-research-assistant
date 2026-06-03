import pickle
from pathlib import Path
from rank_bm25 import BM25Okapi

BM25_INDEX_PATH = "app/core/bm25_index.pkl"


class BM25Service:

    def __init__(self):
        self.documents = []
        self.metadata = []
        self.bm25 = None

    def tokenize(self, text: str):
        return text.lower().split()

    def build_index(self, chunks):
        tokenized_chunks = []
        self.documents = []
        self.metadata = []

        for chunk in chunks:
            text = chunk["chunk_text"]
            tokenized = self.tokenize(text)
            tokenized_chunks.append(tokenized)
            self.documents.append(text)
            self.metadata.append(chunk)

        self.bm25 = BM25Okapi(tokenized_chunks)
        self.save_index()

    def save_index(self):
        data = {
            "documents": self.documents,
            "metadata": self.metadata,
            "bm25": self.bm25
        }
        with open(BM25_INDEX_PATH, "wb") as f:
            pickle.dump(data, f)

    def load_index(self):
        path = Path(BM25_INDEX_PATH)
        if not path.exists():
            return False

        with open(path, "rb") as f:
            data = pickle.load(f)
            self.documents = data["documents"]
            self.metadata = data["metadata"]
            self.bm25 = data["bm25"]
        return True

    def search(self, query: str, limit: int = 10):
        if not self.bm25:
            loaded = self.load_index()
            if not loaded:
                return []

        tokenized_query = self.tokenize(query)
        scores = self.bm25.get_scores(tokenized_query)
        ranked = sorted(
            enumerate(scores),
            key=lambda x: x[1],
            reverse=True
        )

        results = []
        for rank, (idx, score) in enumerate(ranked[:limit]):
            results.append({
                "rank": rank + 1,
                "score": float(score),
                "text": self.documents[idx],
                "metadata": self.metadata[idx]
            })
        return results


bm25_service = BM25Service()
