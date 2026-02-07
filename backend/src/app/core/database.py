"""Database utilities and migration helpers."""

from sqlmodel import SQLModel, Session
from app.api.deps import engine
from app.models import *  # Import all models to register them

def create_all_tables():
    """Create all tables. Use for development/testing only.
    
    For production, use Alembic migrations:
    alembic upgrade head
    """
    SQLModel.metadata.create_all(engine)

def get_session():
    """Get a database session."""
    with Session(engine) as session:
        yield session