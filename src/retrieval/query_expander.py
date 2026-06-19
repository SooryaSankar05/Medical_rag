from src.generation.gemini_client import generate_answer


def expand_query(question):

    prompt = f"""
You are a medical search expert.

Generate 3 alternative search queries that would help retrieve relevant medical information.

Rules:
- Keep queries short.
- Focus on different aspects of the question.
- Return only the queries.
- One query per line.

Question:
{question}
"""

    response = generate_answer(prompt)

    if response == "Gemini request failed.":
        return [question]

    queries = [question]

    for line in response.split("\n"):

        line = line.strip()

        if line:
            queries.append(line)

    return queries