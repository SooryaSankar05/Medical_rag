from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


def retrieve(query_embedding, chunk_embeddings, chunks, top_k=3):

    similarities = cosine_similarity(
        [query_embedding],
        chunk_embeddings
    )[0]

    top_indices = np.argsort(similarities)[-top_k:][::-1]

    results = []

    for idx in top_indices:
        results.append(
            {
                "chunk": chunks[idx],
                "score": similarities[idx]
            }
        )

    return results