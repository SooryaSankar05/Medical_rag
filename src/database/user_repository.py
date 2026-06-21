from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from src.database.db import engine
from src.database.models import User

from src.auth.security import (
    hash_password,
    verify_password
)


def create_user(
    username,
    password
):

    with Session(engine) as session:

        existing_user = session.query(
            User
        ).filter(
            User.username == username
        ).first()

        if existing_user:
            raise ValueError("Username already exists")

        user = User(
            username=username,
            hashed_password=hash_password(
                password
            )
        )

        session.add(user)

        try:
            session.commit()
            session.refresh(user)
            return user
        except IntegrityError:
            session.rollback()
            raise ValueError("Username already exists")
        except SQLAlchemyError as e:
            session.rollback()
            raise e


def get_user_by_username(username):

    with Session(engine) as session:

        user = session.query(
            User
        ).filter(
            User.username == username
        ).first()

        return user


def verify_user_credentials(
    username,
    password
):

    user = get_user_by_username(username)

    if not user:

        return False

    return verify_password(
        password,
        user.hashed_password
    )