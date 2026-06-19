import re
from rank_bm25 import BM25Okapi


STOP_WORDS = {
    "what",
    "is",
    "the",
    "a",
    "an",
    "of",
    "for",
    "in",
    "to",
    "and",
    "on"
}

def build_bm25(metadata):

    documents = []

    for chunk in metadata:

        text = chunk["text"].lower()

        text = re.sub(
            r"[^a-zA-Z0-9\s]",
            "",
            text
        )

        documents.append(
            text.split()
        )

    return BM25Okapi(documents)


def search_bm25(
    bm25,
    query,
    top_k=5
):

    query = query.lower()

    query = re.sub(
        r"[^a-zA-Z0-9\s]",
        "",
        query
    )

    tokenized_query = [
    word
    for word in query.split()
    if word not in STOP_WORDS
]

    scores = bm25.get_scores(
        tokenized_query
    )

    ranked_indices = sorted(
        range(len(scores)),
        key=lambda i: scores[i],
        reverse=True
    )

    return ranked_indices[:top_k]