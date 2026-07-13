from datetime import date

from sqlalchemy import Date, String
from sqlalchemy.orm import Mapped, mapped_column

from models.base import BaseModel


class Guest(BaseModel):
    """
    Guest database model.

    Represents a guest staying at the apartment.
    This model only stores guest data and contains no business logic.
    """

    __tablename__ = "guests"

    # ==========================
    # Guest Information
    # ==========================

    full_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    phone: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    nationality: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    # ==========================
    # Stay Information
    # ==========================

    check_in: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    check_out: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    # ==========================
    # Representation
    # ==========================

    def __repr__(self) -> str:
        return (
            f"Guest("
            f"id={self.id}, "
            f"name='{self.full_name}', "
            f"phone='{self.phone}'"
            f")"
        )