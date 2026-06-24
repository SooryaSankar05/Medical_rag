from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)


def split_text(
    text_or_pages,
    source,
    start_chunk_id=0,
    user_id=None
):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=200
    )

    chunks = []

    # Check if input is new page-based format or old text format
    if isinstance(text_or_pages, list) and len(text_or_pages) > 0 and isinstance(text_or_pages[0], dict):
        # New format: list of pages with page_number and text
        all_text = ""
        page_map = {}  # Maps character position to page number

        current_pos = 0
        for page in text_or_pages:
            page_text = page["text"]
            page_num = page["page_number"]
            all_text += page_text
            # Track which page this text belongs to
            for char_pos in range(len(page_text)):
                page_map[current_pos + char_pos] = page_num
            current_pos += len(page_text)

        raw_chunks = splitter.split_text(all_text)

        for idx, chunk in enumerate(raw_chunks):
            # Find the page number for this chunk (use the first character's page)
            chunk_start_pos = all_text.find(chunk)
            page_number = page_map.get(chunk_start_pos, 1)  # Default to page 1 if not found

            chunks.append(
                {
                    "text": chunk,
                    "source": source,
                    "chunk_id": start_chunk_id + idx,
                    "user_id": user_id,
                    "page_number": page_number
                }
            )
    else:
        # Old format: plain text (backward compatibility)
        raw_chunks = splitter.split_text(text_or_pages)

        for idx, chunk in enumerate(raw_chunks):
            chunks.append(
                {
                    "text": chunk,
                    "source": source,
                    "chunk_id": start_chunk_id + idx,
                    "user_id": user_id,
                    "page_number": None  # No page info for old format
                }
            )

    return chunks