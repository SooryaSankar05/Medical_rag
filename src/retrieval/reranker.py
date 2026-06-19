from sentence_transformers import CrossEncoder

model = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)


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

    ranked = sorted(
        zip(chunks, scores),
        key=lambda x: x[1],
        reverse=True
    )

    return ranked[:top_n]
