import uuid
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, Distance, VectorParams, Filter, FieldCondition, MatchValue

# Initialize Qdrant client pointing to your background Docker container
client = QdrantClient(host="localhost", port=6333)
COLLECTION_NAME = "research_chunks"


def create_collection():
    """
    Creates the master vector indexing collection if it does not exist.
    """
    if not client.collection_exists(collection_name=COLLECTION_NAME):
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=384,  # Matching your local BAAI/bge-small dense dimension vectors size
                distance=Distance.COSINE
            )
        )


def store_embeddings(points_data: list[dict]):
    """
    Converts vector dictionary arrays into Qdrant PointStruct instances and upserts them.
    """
    points = []
    for data in points_data:
        points.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=data["vector"],
                payload={
                    "text": data["text"],
                    **data["metadata"]  # Unpacks workspace_id, document_id, source, page_number, chunk_index
                }
            )
        )
    
    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )


# Upgraded Step 7 Search Service Layer: Accepts an optional workspace isolation filter condition
def search_embeddings(vector: list[float], limit: int = 20, workspace_id: str = None):
    """
    Executes a high-precision cosine similarity look up inside Qdrant,
    optionally locking the query scope down to a single designated workspace id.
    """
    query_filter = None
    
    # Standardized Step 7 payload metadata matching constraint filter condition
    if workspace_id:
        query_filter = Filter(
            must=[
                FieldCondition(
                    key="workspace_id",
                    match=MatchValue(value=workspace_id)
                )
            ]
        )

    results = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=vector,
        query_filter=query_filter,  # 👈 Enforces isolation natively inside Qdrant
        limit=limit,
        with_payload=True
    )
    
    # Format vector outcomes uniformly to align seamlessly with your downstream RRF fusion functions
    formatted_results = []
    for hit in results:
        formatted_results.append({
            "text": hit.payload.get("text", ""),
            "score": hit.score,
            "metadata": {k: v for k, v in hit.payload.items() if k != "text"}
        })
    return formatted_results

# 👈 Appended Step 11 Logic: Deletes all chunks matching a specific file inside Qdrant
def delete_document_chunks(document_id: str):
    """
    Commands Qdrant to locate and permanently purge all vector points 
    matching a targeted document tracking hash using metadata payload filters.
    """
    client.delete(
        collection_name=COLLECTION_NAME,
        points_selector=Filter(
            must=[
                FieldCondition(
                    key="document_id",
                    match=MatchValue(value=document_id)
                )
            ]
        )
    )
