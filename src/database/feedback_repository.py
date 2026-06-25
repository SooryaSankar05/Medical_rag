from sqlalchemy.orm import sessionmaker
from src.database.db import engine
from src.database.models import Feedback

Session = sessionmaker(bind=engine)


def save_feedback(user_id, chat_id, is_positive):
    """Save user feedback for a chat response."""
    session = Session()
    try:
        feedback = Feedback(
            user_id=user_id,
            chat_id=chat_id,
            is_positive=is_positive
        )
        session.add(feedback)
        session.commit()
        return feedback.id
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def get_feedback_by_chat(chat_id):
    """Get feedback for a specific chat."""
    session = Session()
    try:
        feedback = session.query(Feedback).filter_by(chat_id=chat_id).first()
        return feedback
    finally:
        session.close()


def get_user_feedback(user_id):
    """Get all feedback from a user."""
    session = Session()
    try:
        feedback_list = session.query(Feedback).filter_by(user_id=user_id).all()
        return feedback_list
    finally:
        session.close()
