from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=600,       # Increased size slightly for deeper contextual capture
    chunk_overlap=120     # Safe paragraph overlap window
)


def chunk_pages(pages):
    all_chunks = []
    chunk_counter = 0
    seen_texts = set()  # 👈 Strict duplication filter guard

    for page in pages:
        page_number = page["page_number"]
        chunks = splitter.split_text(page["text"])

        for chunk in chunks:
            clean_text = chunk.strip()
            # Skip empty paragraphs or direct text duplicates
            if not clean_text or clean_text in seen_texts:
                continue
                
            seen_texts.add(clean_text)
            all_chunks.append({
                "chunk_text": clean_text,
                "page_number": page_number,
                "chunk_index": chunk_counter
            })
            chunk_counter += 1

    return all_chunks
