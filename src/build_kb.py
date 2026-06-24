from pathlib import Path

from src.ingestion.pdf_loader import extract_text_from_pdf
from src.chunking.text_splitter import split_text

from src.embeddings.chunk_embedder import (
    create_chunk_embeddings
)

from src.retrieval.faiss_store import (
    build_faiss_index,
    save_index
)

from src.retrieval.metadata_store import (
    save_metadata
)
from src.preprocessing.cleaner import remove_references

all_chunks = []

pdf_folder = Path("data/raw")

pdf_files = list(pdf_folder.glob("*.pdf"))

print(f"Found {len(pdf_files)} PDFs\n")

for pdf in pdf_files:

    print(f"Processing: {pdf.name}")

    pages = extract_text_from_pdf(str(pdf))
    pages = remove_references(pages)

    chunks = split_text(
        pages,
        pdf.name,
        start_chunk_id=len(all_chunks),
        user_id=None  # Existing docs are public (accessible to all users)
    )

    all_chunks.extend(chunks)

print(f"\nTotal Chunks: {len(all_chunks)}")

embeddings = create_chunk_embeddings(
    all_chunks
)

print(f"Total Embeddings: {len(embeddings)}")

index = build_faiss_index(
    embeddings
)

save_index(
    index,
    "data/vector_store/medical_index.faiss"
)

save_metadata(
    all_chunks,
    "data/vector_store/metadata.pkl"
)

print("\nKnowledge Base Created Successfully")