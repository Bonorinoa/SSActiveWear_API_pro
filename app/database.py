# app/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pydantic_settings import BaseSettings

# This class reads environment variables from your .env file.
# It's case-insensitive, so DATABASE_URL in your .env file maps to database_url here.
class Settings(BaseSettings):
    database_url: str

    class Config:
        env_file = ".env"

settings = Settings()

# The engine is the central point of contact with the database.
engine = create_engine(settings.database_url)

# SessionLocal instances will be the actual database sessions.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)