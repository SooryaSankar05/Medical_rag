from src.embeddings.embedder import get_embedding


def create_chunk_embeddings(chunks):

    embeddings = []

    for chunk in chunks:
        embeddings.append(
            get_embedding(
                chunk["text"]
            )
        )

    return embeddings