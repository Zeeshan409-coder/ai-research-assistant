from uuid import uuid4
from qdrant_client.models import VectorParams, Distance, PointStruct
from app.db.qdrant import client
from app.models.document_metadata import build_chunk_metadata

COLLECTION_NAME = "research_documents"


def create_collection():
    collections = client.get_collections().collections
    exists = any(col.name == COLLECTION_NAME for col in collections)

    if not exists:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE),
        )


def store_document_chunks(chunks, filename, document_id, embedding_function):
    points = []
    total_chunks = len(chunks)

    for chunk in chunks:
        # Generate the math concept vector for the clean chunk text snippet
        embedding = embedding_function(chunk["chunk_text"])

        # Construct the detailed production metadata package
        metadata = build_chunk_metadata(
            filename=filename,
            document_id=document_id,
            chunk=chunk,
            total_chunks=total_chunks
        )

        points.append(
            PointStruct(
                id=str(uuid4()),
                vector=embedding,
                payload=metadata
            )
        )

    client.upsert(collection_name=COLLECTION_NAME, points=points)
