from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from config import settings


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy models.
    """
    pass


engine = create_engine(
    settings.DATABASE_URL,
    echo=False,
)


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False
)


def get_db():
    """
    Creates a database session for each request.
    """

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()
