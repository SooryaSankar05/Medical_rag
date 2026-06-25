from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from src.database.db import engine
from src.database.models import QueryAnalytics

Session = sessionmaker(bind=engine)


def save_query_analytics(user_id, question, retrieval_time=None, generation_time=None, 
                         total_time=None, confidence=None, num_sources=None):
    """Save query analytics."""
    session = Session()
    try:
        analytics = QueryAnalytics(
            user_id=user_id,
            question=question,
            retrieval_time=retrieval_time,
            generation_time=generation_time,
            total_time=total_time,
            confidence=confidence,
            num_sources=num_sources
        )
        session.add(analytics)
        session.commit()
        return analytics.id
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def get_analytics_stats():
    """Get overall analytics statistics."""
    session = Session()
    try:
        total_queries = session.query(func.count(QueryAnalytics.id)).scalar()
        
        avg_retrieval_time = session.query(func.avg(QueryAnalytics.retrieval_time)).scalar()
        avg_generation_time = session.query(func.avg(QueryAnalytics.generation_time)).scalar()
        avg_total_time = session.query(func.avg(QueryAnalytics.total_time)).scalar()
        avg_confidence = session.query(func.avg(QueryAnalytics.confidence)).scalar()
        
        return {
            "total_queries": total_queries or 0,
            "avg_retrieval_time": round(avg_retrieval_time, 3) if avg_retrieval_time else 0,
            "avg_generation_time": round(avg_generation_time, 3) if avg_generation_time else 0,
            "avg_total_time": round(avg_total_time, 3) if avg_total_time else 0,
            "avg_confidence": round(avg_confidence, 3) if avg_confidence else 0
        }
    finally:
        session.close()


def get_user_analytics(user_id):
    """Get analytics for a specific user."""
    session = Session()
    try:
        user_queries = session.query(func.count(QueryAnalytics.id)).filter_by(user_id=user_id).scalar()
        
        avg_retrieval_time = session.query(func.avg(QueryAnalytics.retrieval_time)).filter_by(user_id=user_id).scalar()
        avg_generation_time = session.query(func.avg(QueryAnalytics.generation_time)).filter_by(user_id=user_id).scalar()
        avg_total_time = session.query(func.avg(QueryAnalytics.total_time)).filter_by(user_id=user_id).scalar()
        avg_confidence = session.query(func.avg(QueryAnalytics.confidence)).filter_by(user_id=user_id).scalar()
        
        return {
            "user_queries": user_queries or 0,
            "avg_retrieval_time": round(avg_retrieval_time, 3) if avg_retrieval_time else 0,
            "avg_generation_time": round(avg_generation_time, 3) if avg_generation_time else 0,
            "avg_total_time": round(avg_total_time, 3) if avg_total_time else 0,
            "avg_confidence": round(avg_confidence, 3) if avg_confidence else 0
        }
    finally:
        session.close()
