from sentence_transformers import CrossEncoder
import re

model = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)


def has_definition_pattern(text):
    """Check if text contains definition-like patterns."""
    definition_patterns = [
        r'\bis defined as\b',
        r'\brefers to\b',
        r'\bis a\b',
        r'\brefers to the\b',
        r'\bdefined as\b',
        r'\bmeans\b',
        r'\bcan be defined as\b',
        r'\bdescribed as\b'
    ]
    
    text_lower = text.lower()
    for pattern in definition_patterns:
        if re.search(pattern, text_lower):
            return True
    return False


def rerank(
    question,
    chunks,
    top_n=3
):

    pairs = []

    for chunk in chunks:

        pairs.append(
            [question, chunk["text"]]
        )

    scores = model.predict(pairs)

    # Apply definition boost
    boosted_scores = []
    for chunk, score in zip(chunks, scores):
        boost = 0.2 if has_definition_pattern(chunk["text"]) else 0
        boosted_scores.append((chunk, score + boost))

    ranked = sorted(
        boosted_scores,
        key=lambda x: x[1],
        reverse=True
    )

    return ranked[:top_n]
