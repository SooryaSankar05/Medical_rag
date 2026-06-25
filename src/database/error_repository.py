from sqlalchemy.orm import sessionmaker
from src.database.db import engine
from src.database.models import ErrorLog

Session = sessionmaker(bind=engine)


def log_error(user_id, error_type, error_message, stack_trace=None):
    """Log an error to the database."""
    session = Session()
    try:
        error_log = ErrorLog(
            user_id=user_id,
            error_type=error_type,
            error_message=error_message,
            stack_trace=stack_trace
        )
        session.add(error_log)
        session.commit()
        return error_log.id
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def get_recent_errors(limit=10):
    """Get recent error logs."""
    session = Session()
    try:
        errors = session.query(ErrorLog).order_by(ErrorLog.created_at.desc()).limit(limit).all()
        return errors
    finally:
        session.close()


def get_user_errors(user_id, limit=10):
    """Get recent errors for a specific user."""
    session = Session()
    try:
        errors = session.query(ErrorLog).filter_by(user_id=user_id).order_by(ErrorLog.created_at.desc()).limit(limit).all()
        return errors
    finally:
        session.close()
