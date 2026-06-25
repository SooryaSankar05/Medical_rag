from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    DateTime,
    Float,
    Boolean
)
from sqlalchemy.sql import func

from sqlalchemy.orm import (
    declarative_base
)

Base = declarative_base()


class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True
    )

    username = Column(
        String,
        unique=True,
        nullable=False
    )

    hashed_password = Column(
    String,
    nullable=False
    )


class ChatHistory(Base):

    __tablename__ = "chat_history"

    id = Column(
        Integer,
        primary_key=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    question = Column(
        Text,
        nullable=False
    )

    answer = Column(
        Text,
        nullable=False
    )

    sources = Column(
        Text,
        nullable=True
    )

    confidence = Column(
        Float,
        nullable=True
    )

    created_at = Column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )


class Document(Base):

    __tablename__ = "documents"

    id = Column(
        Integer,
        primary_key=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    filename = Column(
        String,
        nullable=False
    )

    filepath = Column(
        String,
        nullable=False
    )

    uploaded_at = Column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )


class Feedback(Base):

    __tablename__ = "feedback"

    id = Column(
        Integer,
        primary_key=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    chat_id = Column(
        Integer,
        ForeignKey("chat_history.id"),
        nullable=False
    )

    is_positive = Column(
        Boolean,
        nullable=False
    )

    created_at = Column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )


class QueryAnalytics(Base):

    __tablename__ = "query_analytics"

    id = Column(
        Integer,
        primary_key=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    question = Column(
        Text,
        nullable=False
    )

    retrieval_time = Column(
        Float,
        nullable=True
    )

    generation_time = Column(
        Float,
        nullable=True
    )

    total_time = Column(
        Float,
        nullable=True
    )

    confidence = Column(
        Float,
        nullable=True
    )

    num_sources = Column(
        Integer,
        nullable=True
    )

    created_at = Column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )


class ErrorLog(Base):

    __tablename__ = "error_logs"

    id = Column(
        Integer,
        primary_key=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )

    error_type = Column(
        String,
        nullable=False
    )

    error_message = Column(
        Text,
        nullable=False
    )

    stack_trace = Column(
        Text,
        nullable=True
    )

    created_at = Column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )