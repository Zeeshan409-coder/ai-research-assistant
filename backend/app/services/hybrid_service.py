from collections import defaultdict
from app.services.retrieval_service import search_documents
from app.services.bm25_service import bm25_service
from app.services.reranker_service import rerank_documents  

RRF_K = 60


def reciprocal_rank_fusion(dense_results, sparse_results, limit=20):
    scores = defaultdict(float)
    documents = {}

    # 1. Process Dense Vector Rankings from Qdrant
    for rank, result in enumerate(dense_results):
        doc_id = (
            result.payload["document_id"],
            result.payload["chunk_index"]
        )
        scores[doc_id] += 1 / (RRF_K + rank + 1)
        documents[doc_id] = {
            "text": result.payload["text"],
            "metadata": result.payload,
            "dense_score": result.score
        }

    # 2. Process Sparse Keyword Rankings from BM25
    for rank, result in enumerate(sparse_results):
        metadata = result["metadata"]
        doc_id = (
            metadata["document_id"],
            metadata["chunk_index"]
        )
        scores[doc_id] += 1 / (RRF_K + rank + 1)
        documents[doc_id] = {
            "text": result["text"],
            "metadata": metadata,
            "sparse_score": result["score"]
        }

    # 3. Sort candidates by combined RRF score index
    reranked = sorted(
        scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    fused_results = []
    # Cleaned: standard slice loop syntax to prevent SyntaxErrors
    for doc_id, rrf_score in reranked[:limit]:
        doc = documents[doc_id]
        fused_results.append({
            "rrf_score": rrf_score,
            "text": doc["text"],
            "metadata": doc["metadata"]
        })

    return fused_results


def hybrid_search(query: str, limit: int = 5):
    # 1. Expand candidate net to top 20 vectors for wider coverage
    dense_results = search_documents(query=query, limit=20)
    
    # 2. Expand candidate net to top 20 keywords for exact matches
    sparse_results = bm25_service.search(query=query, limit=20)
    
    # 3. Fuse lists together statistically via RRF
    fused = reciprocal_rank_fusion(
        dense_results=dense_results,
        sparse_results=sparse_results,
        limit=20
    )

    # 4. Neural Cross-Encoder Reranking to isolate top best context blocks
    reranked = rerank_documents(
        query=query,
        documents=fused,
        top_k=limit
    )

    return reranked
