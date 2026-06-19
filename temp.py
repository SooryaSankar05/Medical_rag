from sqlalchemy import inspect
from src.database.db import engine

print(
    inspect(engine).get_columns("users")
)