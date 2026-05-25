from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

POSTGRES_DB_URL = "postgresql+psycopg://postgres:password@postgres:5432/ai-assistant-db"

engine = create_engine(url=POSTGRES_DB_URL)

SessionLocal = sessionmaker(bind=engine, autoflush=False)

