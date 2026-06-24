import os
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from src.database.db import engine
from src.database.models import Document


def save_document(
    user_id,
    filename,
    filepath
):

    with Session(engine) as session:

        # Check for duplicate filename for the same user
        existing_document = session.query(
            Document
        ).filter(
            Document.user_id == user_id,
            Document.filename == filename
        ).first()

        if existing_document:
            raise ValueError("Document already uploaded")

        document = Document(
            user_id=user_id,
            filename=filename,
            filepath=filepath
        )

        try:
            session.add(document)
            session.commit()
            session.refresh(document)
            return document
        except SQLAlchemyError as e:
            session.rollback()
            raise e


def get_documents_by_user(user_id):

    with Session(engine) as session:

        documents = session.query(
            Document
        ).filter(
            Document.user_id == user_id
        ).order_by(
            Document.uploaded_at.desc()
        ).all()

        return documents


def delete_document(document_id, user_id):

    with Session(engine) as session:

        document = session.query(
            Document
        ).filter(
            Document.id == document_id
        ).first()

        if not document:
            return False

        # Verify ownership
        if document.user_id != user_id:
            raise PermissionError("You do not have permission to delete this document")

        filepath = document.filepath

        try:
            session.delete(document)
            session.commit()

            # Delete the actual file
            if os.path.exists(filepath):
                os.remove(filepath)

            # TODO: Future phases must also clean up:
            # - chunks associated with this document
            # - embeddings for those chunks
            # - retrieval metadata
            # - vector entries in FAISS index

            return True
        except SQLAlchemyError as e:
            session.rollback()
            raise e


def get_document_by_id(document_id):

    with Session(engine) as session:

        document = session.query(
            Document
        ).filter(
            Document.id == document_id
        ).first()

        return document
