from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=600,       # Increased size slightly for deeper contextual capture
    chunk_overlap=120     # Safe paragraph overlap window
)


def chunk_pages(pages, workspace_id: str, document_id: str, filename: str):
    """
    Splits document pages into paragraphs and tags each chunk with an advanced,
    workspace-scoped metadata tracking layout payload.
    """
    all_chunks = []
    chunk_counter = 0
    seen_texts = set()  # Strict duplication filter guard

    for page in pages:
        page_number = page["page_number"]
        chunks = splitter.split_text(page["text"])

        for chunk in chunks:
            clean_text = chunk.strip()
            # Skip empty paragraphs or direct text duplicates
            if not clean_text or clean_text in seen_texts:
                continue
                
            seen_texts.add(clean_text)
            
            # Upgraded Step 3 Metadata Layout Mapping Structure
            metadata = {
                "workspace_id": workspace_id,
                "document_id": document_id,
                "source": filename,
                "page_number": page_number,
                "chunk_index": chunk_counter
            }
            
            all_chunks.append({
                "chunk_text": clean_text,
                "metadata": metadata
            })
            chunk_counter += 1

    return all_chunks
