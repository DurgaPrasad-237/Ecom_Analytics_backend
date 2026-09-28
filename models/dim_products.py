from datetime import date

from sqlalchemy import Date, Integer, Float, String
from sqlalchemy.orm import Mapped, mapped_column

from DB.db_config import Base


class DimProduct(Base):
    __tablename__ = "dim_product"

    product_id: Mapped[str] = mapped_column(
        String(20),
        primary_key=True
    )

    product_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    category: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    subcategory: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    brand: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    price: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    cost_price: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    discount_range: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    rating_average: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    rating_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    stock_quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    product_launch_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    product_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    return_rate_baseline: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )