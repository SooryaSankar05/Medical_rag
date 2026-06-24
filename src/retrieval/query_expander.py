from src.generation.gemini_client import generate_answer


def expand_query(question):

    # Check if it's a definition-style question
    is_definition = question.lower().startswith("what is") or question.lower().startswith("what are")

    if is_definition:
        # For definition questions, add specific definition-focused queries
        definition_queries = []
        
        # Extract the term being defined
        if "what is" in question.lower():
            term = question.lower().replace("what is", "").replace("?", "").strip()
            definition_queries.append(f"{term} definition")
            definition_queries.append(f"{term} defined as")
            definition_queries.append(f"definition of {term}")
        elif "what are" in question.lower():
            term = question.lower().replace("what are", "").replace("?", "").strip()
            definition_queries.append(f"{term} definition")
            definition_queries.append(f"{term} defined as")
            definition_queries.append(f"definition of {term}")
        
        # Use these as the expanded queries
        return [question] + definition_queries[:3]

    # For non-definition questions, use Gemini to generate queries
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