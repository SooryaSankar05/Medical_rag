import faiss
import numpy as np


def build_faiss_index(embeddings):

    embeddings = np.array(
        embeddings,
        dtype=np.float32
    )

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(embeddings)

    return index


def save_index(index, path):
    faiss.write_index(index, path)


def load_index(path):
    return faiss.read_index(path)


def search_faiss(index, query_embedding, top_k=3):

    query_embedding = np.array(
        [query_embedding],
        dtype=np.float32
    )

    distances, indices = index.search(
        query_embedding,
        top_k
    )

    for i, idx in enumerate(indices[0]):
        print(f"Score: {distances[0][i]:.4f}")

    return distances, indices