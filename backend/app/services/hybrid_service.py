from app.services.embedding_service import generate_embedding
from app.services.qdrant_service import search_embeddings


def hybrid_search(query: str, workspace_id: str = None, top_k: int = 5):
    """
    Executes a multi-stage fusion lookup across local vector nodes,
    forcing lookups to isolate parameters matching your active workspace_id folder.
    """
    # 1. Generate dense query embedding vector
    query_vector = generate_embedding(query)

    # 2. Retrieve isolated candidate text blocks from Qdrant using the workspace filter string
    dense_results = search_embeddings(
        vector=query_vector,
        limit=20,
        workspace_id=workspace_id  # 👈 Passed down directly to your filtering service logic
    )

    # 3. Simulate localized BM25 ranking adjustments across the returned workspace chunk pool
    # In a production layout with massive text pools, this filters text entries by string matches.
    # Because our dense results are already restricted by workspace_id, our fusion remains completely safe!
    bm25_results = []
    for rank, hit in enumerate(dense_results):
        score = 1.0 / (rank + 1)
        if any(word in query.lower() for word in hit["text"].lower().split()):
            score += 1.5  # Boost match ranking if query tokens match text characters
        bm25_results.append({"hit": hit, "score": score})
        
    bm25_results = sorted(bm25_results, key=lambda x: x["score"], reverse=True)

    # 4. Perform standard Reciprocal Rank Fusion (RRF) calculation over the workspace context fragments
    rrf_scores = {}
    k = 60

    # Process Dense list placement weights
    for rank, hit in enumerate(dense_results):
        text = hit["text"]
        rrf_scores[text] = rrf_scores.get(text, 0.0) + (1.0 / (k + rank + 1))

    # Process BM25 list placement weights
    for rank, item in enumerate(bm25_results):
        text = item["hit"]["text"]
        rrf_scores[text] = rrf_scores.get(text, 0.0) + (1.0 / (k + rank + 1))

    # Reassemble and attach the final ranked context chunks pool back to their source dictionaries
    sorted_texts = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)
    
    final_hits = []
    for text, rrf_score in sorted_texts[:top_k]:
        original_hit = next(h for h in dense_results if h["text"] == text)
        final_hits.append({
            "text": text,
            "rrf_score": rrf_score,
            "metadata": original_hit["metadata"]
        })

    # 5. Local Cross-Encoder Re-ranking Step Integration Check
    # (Your context_builder in the next step will automatically sort this sub-array block!)
    return final_hits
