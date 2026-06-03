from fastapi import APIRouter, UploadFile, File
import shutil
from pathlib import Path

from app.services.pdf_service import extract_text_by_page
from app.services.chunk_service import chunk_pages
from app.services.embedding_service import generate_embedding
from app.services.qdrant_service import store_document_chunks
from app.services.bm25_service import bm25_service  
from app.utils.id_generator import generate_document_id

router = APIRouter()

UPLOAD_DIR = "uploads"


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    document_id = generate_document_id()
    file_path = Path(UPLOAD_DIR) / file.filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 1. Extract raw page text blocks page by page
    pages = extract_text_by_page(str(file_path))

    # 2. Slice text into sequential chunks
    chunks = chunk_pages(pages)

    # 3. Enrich the text chunks list with metadata tracking attributes
    # This injects the document_id so BM25 and Qdrant layouts are identical!
    for chunk in chunks:
        chunk["document_id"] = document_id
        chunk["source"] = file.filename

    # 4. Build the local keyword index mapping using the enriched chunks
    bm25_service.build_index(chunks)

    # 5. Ship the matching vector records right into your Qdrant container
    store_document_chunks(
        chunks=chunks,
        filename=file.filename,
        document_id=document_id,
        embedding_function=generate_embedding
    )

    return {
        "document_id": document_id,
        "filename": file.filename,
        "pages": len(pages),
        "chunks_stored": len(chunks),
        "status": "success"
    }
