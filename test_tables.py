from sqlalchemy import inspect
from src.database.db import engine

inspector = inspect(engine)

print(inspector.get_table_names())