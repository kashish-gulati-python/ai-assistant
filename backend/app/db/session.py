from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

POSTGRES_DB_URL = os.getenv("DATABASE_URL", "postgresql+psycopg://postgres:password@localhost:5432/ai-assistant-db")

engine = create_engine(url=POSTGRES_DB_URL)

SessionLocal = sessionmaker(bind=engine, autoflush=False)

