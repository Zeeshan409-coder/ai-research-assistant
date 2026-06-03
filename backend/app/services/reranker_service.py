from sentence_transformers import CrossEncoder

# Pointing straight to the folder where your 5 downloaded files live
LOCAL_MODEL_PATH = "app/core/bge-reranker-base"
model = CrossEncoder(LOCAL_MODEL_PATH)


def rerank_documents(query: str, documents: list, top_k: int = 5):
    if not documents:
        return []

    pairs = [(query, doc["text"]) for doc in documents]
    scores = model.predict(pairs)

    reranked = []
    for doc, score in zip(documents, scores):
        doc["rerank_score"] = float(score)
        reranked.append(doc)

    reranked.sort(key=lambda x: x["rerank_score"], reverse=True)
    return reranked[:top_k]
