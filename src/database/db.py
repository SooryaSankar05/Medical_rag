from sqlalchemy import create_engine

DATABASE_URL = (
    "postgresql://postgres:Soorya_321@localhost:5433/medical_rag"
)

engine = create_engine(
    DATABASE_URL
)

print(
    "Database Connected"
)