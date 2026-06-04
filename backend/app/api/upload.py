import io
from uuid import uuid4
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pypdf import PdfReader

from app.db.dependencies import get_db
from app.models.workspace import Workspace
from app.models.document import Document
from app.services.chunk_service import chunk_pages
from app.services.embedding_service import generate_embedding
from app.services.qdrant_service import store_embeddings, delete_document_chunks  # 👈 Imported your new vector purge tool

router = APIRouter(tags=["Document Ingestion"])


@router.post("/workspaces/{workspace_id}/upload")
async def upload_document(
    workspace_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    workspace = db.query(Workspace).filter(Workspace.id == workspace_id).first()
    if not workspace:
        raise HTTPException(status_code=404, detail="Target workspace container not found")

    try:
        file_bytes = await file.read()
        pdf_file = io.BytesIO(file_bytes)
        reader = PdfReader(pdf_file)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse inbound PDF document: {e}")

    pages = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        pages.append({"page_number": i + 1, "text": text})

    document_id = str(uuid4())
    chunks = chunk_pages(pages=pages, workspace_id=workspace_id, document_id=document_id, filename=file.filename)

    if not chunks:
        raise HTTPException(status_code=400, detail="No readable text chunks could be extracted from this document layout")

    db_document = Document(
        id=document_id,
        workspace_id=workspace_id,
        filename=file.filename,
        total_pages=len(reader.pages),
        total_chunks=len(chunks)
    )
    db.add(db_document)
    db.commit()

    points = []
    for chunk in chunks:
        vector = generate_embedding(chunk["chunk_text"])
        points.append({
            "text": chunk["chunk_text"],
            "vector": vector,
            "metadata": chunk["metadata"]
        })

    store_embeddings(points)

    return {
        "status": "success",
        "message": f"Document '{file.filename}' successfully ingested into workspace context.",
        "document_id": document_id,
        "metrics": {
            "total_pages": len(reader.pages),
            "total_chunks": len(chunks)
        }
    }


# 👈 Added Step 11 Route: Wipes files completely out of both relational and vector storage
@router.delete("/documents/{document_id}", status_code=status.HTTP_200_OK)
def purge_document_file(document_id: str, db: Session = Depends(get_db)):
    """
    Permanently removes a document tracker row entry from PostgreSQL and 
    purges all its associated dense text chunks out of Qdrant vector memory.
    """
    # 1. Search for the master document entry row inside PostgreSQL
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Target document entity not found or already deleted")

    # 2. Trigger the targeted metadata payload chunk selector purge inside Qdrant
    try:
        delete_document_chunks(document_id=document_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to clear vector chunks out of Qdrant indexes: {e}")

    # 3. Delete the primary row registration instance out of PostgreSQL table memory
    db.delete(document)
    db.commit()

    return {
        "status": "success",
        "message": "Document record and all associated vector index entities have been successfully purged."
    }
