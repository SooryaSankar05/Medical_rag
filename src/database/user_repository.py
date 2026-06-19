from sqlalchemy.orm import Session

from src.database.db import engine
from src.database.models import User

from src.auth.security import (
    hash_password
)


def create_user(
    username,
    password
):

    with Session(engine) as session:

        user = User(
            username=username,
            hashed_password=hash_password(
                password
            )
        )

        session.add(user)

        session.commit()