from sqlalchemy import create_engine

DATABASE_URL = (
    "postgresql://postgres:soorya_123@localhost:5432/medical_rag_v2"
)

engine = create_engine(
    DATABASE_URL
)

print(
    "Database Connected"
)