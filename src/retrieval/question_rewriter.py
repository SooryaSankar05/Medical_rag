from src.generation.gemini_client import generate_answer


def rewrite_question(
    question,
    chat_history
):

    if not chat_history:
        return question

    history_text = ""

    for msg in chat_history[-3:]:

        history_text += (
            f"User: {msg['question']}\n"
            f"Assistant: {msg['answer']}\n\n"
        )

    prompt = f"""
Rewrite the current question as a standalone question.

Conversation:

{history_text}

Current Question:
{question}

Return only the rewritten question.
"""

    rewritten = generate_answer(
        prompt
    )

    if rewritten == "Gemini request failed.":
        return question

    return rewritten.strip()