from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class BaseModel(Base):
    """
    Abstract base model.

    Provides common fields shared by all database models.
    """

    __abstract__ = True

    # ==========================
    # Primary Key
    # ==========================

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    # ==========================
    # Metadata
    # ==========================

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )