from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)


def split_text(
    text,
    source,
    start_chunk_id=0,
    user_id=None
):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=200
    )

    raw_chunks = splitter.split_text(
        text
    )

    chunks = []

    for idx, chunk in enumerate(
        raw_chunks
    ):

        chunks.append(
            {
                "text": chunk,
                "source": source,
                "chunk_id": start_chunk_id + idx,
                "user_id": user_id
            }
        )

    return chunks