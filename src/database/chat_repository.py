import json
import numpy as np
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from src.database.db import engine
from src.database.models import ChatHistory


def convert_to_serializable(obj):
    """Convert numpy types and other non-serializable objects to Python native types."""
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {key: convert_to_serializable(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_serializable(item) for item in obj]
    else:
        return obj


def save_chat(
    user_id,
    question,
    answer,
    sources,
    confidence=None
):

    with Session(engine) as session:

        # Convert sources to JSON-serializable format
        serializable_sources = convert_to_serializable(sources) if sources else None

        chat = ChatHistory(
            user_id=user_id,
            question=question,
            answer=answer,
            sources=json.dumps(serializable_sources) if serializable_sources else None,
            confidence=confidence
        )

        try:
            session.add(chat)
            session.commit()
            session.refresh(chat)
            return chat
        except SQLAlchemyError as e:
            session.rollback()
            raise e


def load_chat(user_id):

    with Session(engine) as session:

        chats = session.query(
            ChatHistory
        ).filter(
            ChatHistory.user_id == user_id
        ).order_by(
            ChatHistory.created_at.desc()
        ).all()

        result = []

        for chat in chats:

            sources = json.loads(chat.sources) if chat.sources else []

            result.append({
                "db_id": chat.id,
                "question": chat.question,
                "answer": chat.answer,
                "sources": sources,
                "confidence": chat.confidence
            })

        return result


def clear_chat(user_id):

    with Session(engine) as session:

        try:
            session.query(
                ChatHistory
            ).filter(
                ChatHistory.user_id == user_id
            ).delete()

            session.commit()
            return True
        except SQLAlchemyError as e:
            session.rollback()
            raise e
