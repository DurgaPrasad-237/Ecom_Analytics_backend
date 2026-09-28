from datetime import date

from sqlalchemy import Date, Integer, Float, String
from sqlalchemy.orm import Mapped, mapped_column

from DB.db_config import Base


class DimCustomer(Base):
    __tablename__ = "dim_customer"

    customer_id: Mapped[str] = mapped_column(
        String(20),
        primary_key=True
    )

    customer_signup_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    gender: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    age: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    age_group: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    state: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    city: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    customer_segment: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    preferred_device: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    preferred_payment_method: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    acquisition_channel: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    total_orders: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    total_spend: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    last_order_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )

    average_order_value: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    customer_status: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    loyalty_tier: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )