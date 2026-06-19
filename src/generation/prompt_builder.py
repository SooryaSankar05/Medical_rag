def build_prompt(question, chunks):

    context = "\n\n".join(chunks)

    return f"""
You are an evidence-based medical research assistant.

Answer ONLY from the supplied context.

Response format:

Definition:
Provide a direct answer.

Key Findings:
- Point 1
- Point 2
- Point 3

Clinical Relevance:
Explain why it matters.

If the answer cannot be found in the context, reply exactly:

"I could not find the answer in the provided documents."

Context:
{context}

Question:
{question}

Answer:
"""