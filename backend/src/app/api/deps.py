from typing import Generator
from sqlmodel import Session, create_engine
from app.core.config import settings
import logging

# Configure logger for database operations
logger = logging.getLogger(__name__)

# Create engine from DATABASE_URL (PostgreSQL/Neon or SQLite)
_db_url = settings.DATABASE_URL
_connect_args = {}
if _db_url.startswith("sqlite"):
    _connect_args["check_same_thread"] = False
elif _db_url.startswith("postgresql"):
    # Neon/PostgreSQL: ensure SSL is used when required by URL
    _connect_args = {}

engine = create_engine(
    _db_url,
    connect_args=_connect_args if _connect_args else {},
    echo=settings.DEBUG,
    pool_pre_ping=True,
)

def get_db() -> Generator:
    logger.debug("Creating database session...")
    try:
        with Session(engine) as session:
            logger.debug("Database session created successfully")
            yield session
            logger.debug("Database session closed successfully")
    except Exception as e:
        logger.error(f"Database session error: {str(e)}")
        raise
