from datetime import datetime


def build_chunk_metadata(
    filename,
    document_id,
    chunk,
    total_chunks
):

    return {
        "text": chunk["chunk_text"],
        "source": filename,
        "document_id": document_id,
        "page_number": chunk["page_number"],
        "chunk_index": chunk["chunk_index"],
        "total_chunks": total_chunks,
        "upload_timestamp": datetime.utcnow().isoformat(),
        "content_type": "pdf",
        "collection": "default",
        "embedding_model": "bge-small-en-v1.5"
    }
