from src.embeddings.embedder import get_embedding

from src.retrieval.faiss_store import (
    load_index,
    search_faiss
)

from src.retrieval.metadata_store import (
    load_metadata
)

from src.retrieval.reranker import rerank

from src.generation.prompt_builder import (
    build_prompt
)

from src.generation.gemini_client import (
    generate_answer
)

from src.retrieval.query_expander import (
    expand_query
)

from src.retrieval.bm25_retriever import (
    build_bm25,
    search_bm25
)

from src.retrieval.question_rewriter import (
    rewrite_question
)

# =========================
# Load Once
# =========================

index = load_index(
    "data/vector_store/medical_index.faiss"
)

metadata = load_metadata(
    "data/vector_store/metadata.pkl"
)

# Print counts for debugging
print(f"[DEBUG] FAISS index size: {index.ntotal}")
print(f"[DEBUG] Metadata count: {len(metadata)}")

bm25 = build_bm25(
    metadata
)

# =========================
# Main Pipeline
# =========================

def ask_question(
    question,
    chat_history=None,
    user_id=None
):

    # =========================
    # Rewrite Follow-up Questions
    # =========================

    standalone_question = rewrite_question(
        question,
        chat_history
    )

    print("\nSTANDALONE QUESTION:")
    print(standalone_question)

    # =========================
    # Query Expansion
    # =========================

    expanded_queries = expand_query(
        standalone_question
    )

    # =========================
    # Hybrid Retrieval
    # =========================

    print("[RETRIEVAL] Starting hybrid retrieval")
    all_indices = set()

    for query in expanded_queries:

        query_embedding = get_embedding(
            query
        )

        distances, faiss_indices = search_faiss(
            index,
            query_embedding,
            top_k=10
        )

        for idx in faiss_indices[0]:

            all_indices.add(
                int(idx)
            )

        bm25_indices = search_bm25(
            bm25,
            query,
            top_k=10
        )

        for idx in bm25_indices:

            all_indices.add(
                int(idx)
            )

    # =========================
    # Indices -> Chunks
    # =========================

    retrieved_chunks = []

    for idx in all_indices:

        # Defensive validation: skip invalid indices
        if idx >= len(metadata):
            print(f"[WARNING] Skipping invalid index {idx} (metadata count: {len(metadata)})")
            continue

        chunk = metadata[idx]

        # User isolation: filter by user_id if provided
        # Chunks with user_id=None are public and accessible to all users
        if user_id is not None:
            chunk_user_id = chunk.get("user_id")
            if chunk_user_id is not None and chunk_user_id != user_id:
                continue

        retrieved_chunks.append(chunk)

    # =========================
    # Reranking
    # =========================

    reranked_chunks = rerank(
        standalone_question,
        retrieved_chunks,
        top_n=3
    )

    # =========================
    # Context Creation
    # =========================

    context_chunks = []

    for chunk, score in reranked_chunks:

        context_chunks.append(
            chunk["text"]
        )

    # =========================
    # Prompt
    # =========================

    prompt = build_prompt(
        standalone_question,
        context_chunks
    )

    # =========================
    # Gemini
    # =========================

    print("[GENERATION] Generating answer with Gemini")
    answer = generate_answer(
        prompt
    )

    # =========================
    # Sources
    # =========================

    sources = []

    for chunk, score in reranked_chunks:

        sources.append(
            {
                "pdf": chunk["source"],
                "chunk": chunk["chunk_id"],
                "score": round(
                    score,
                    4
                ),
                "preview": chunk["text"][:300]
            }
        )

    return answer, sources