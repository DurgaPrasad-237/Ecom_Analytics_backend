from datetime import date

from sqlalchemy import Date, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from DB.db_config import Base


class DimDate(Base):
    __tablename__ = "dim_date"

    date_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    full_date: Mapped[date] = mapped_column(
        Date,
        unique=True,
        nullable=False
    )

    day: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    month: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    month_name: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    quarter: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    year: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    week: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    day_name: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )