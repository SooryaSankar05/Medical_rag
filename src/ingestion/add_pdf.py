from src.ingestion.pdf_loader import (
    extract_text_from_pdf
)

from src.chunking.text_splitter import (
    split_text
)

from src.embeddings.chunk_embedder import (
    create_chunk_embeddings
)

from src.retrieval.faiss_store import (
    load_index,
    save_index
)

from src.retrieval.metadata_store import (
    load_metadata,
    save_metadata
)

from src.preprocessing.cleaner import (
    remove_references
)

import numpy as np


def add_pdf(pdf_path, user_id=None):

    print(
        f"Processing: {pdf_path}"
    )

    # =========================
    # Extract Text
    # =========================

    text = extract_text_from_pdf(
        pdf_path
    )

    text = remove_references(
        text
    )

    pdf_name = pdf_path.split("\\")[-1]

    # =========================
    # Load Existing Metadata
    # =========================

    metadata = load_metadata(
        "data/vector_store/metadata.pkl"
    )

    next_chunk_id = len(
        metadata
    )

    # =========================
    # Chunking
    # =========================

    chunks = split_text(
        text,
        pdf_name,
        start_chunk_id=next_chunk_id,
        user_id=user_id
    )

    # =========================
    # Embeddings
    # =========================

    embeddings = create_chunk_embeddings(
        chunks
    )

    embeddings = np.array(
        embeddings,
        dtype=np.float32
    )

    # =========================
    # Load Existing FAISS
    # =========================

    index = load_index(
        "data/vector_store/medical_index.faiss"
    )

    index.add(
        embeddings
    )

    save_index(
        index,
        "data/vector_store/medical_index.faiss"
    )

    # =========================
    # Update Metadata
    # =========================

    metadata.extend(
        chunks
    )

    save_metadata(
        metadata,
        "data/vector_store/metadata.pkl"
    )

    print(
        f"Added {len(chunks)} chunks"
    )

    print(
        f"Total Chunks: {len(metadata)}"
    )