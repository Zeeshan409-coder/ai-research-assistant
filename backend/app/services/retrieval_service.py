from app.db.qdrant import client
from app.services.embedding_service import generate_embedding

COLLECTION_NAME = "research_documents"


def search_documents(query: str, limit: int = 5):

    query_embedding = generate_embedding(query)

    # Updated from .search() to the modern .query_points() method
    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_embedding,
        limit=limit
    )

    return results.points
