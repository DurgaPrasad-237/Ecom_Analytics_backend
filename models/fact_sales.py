from typing import Optional

from sqlalchemy import String, Integer, Float, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from DB.db_config import Base


class FactSales(Base):

    __tablename__ = "fact_sales"

    # ============================================================
    # PRIMARY KEY
    # ============================================================

    order_item_id: Mapped[str] = mapped_column(
        String(50),
        primary_key=True
    )

    # ============================================================
    # FOREIGN KEYS / IDENTIFIERS
    # ============================================================

    order_id: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    product_id: Mapped[str] = mapped_column(
        String(50),
        ForeignKey("dim_product.product_id"),
        nullable=False
    )

    customer_id: Mapped[str] = mapped_column(
        String(50),
        ForeignKey("dim_customer.customer_id"),
        nullable=False
    )

    shipment_id: Mapped[Optional[str]] = mapped_column(
        String(50),
        ForeignKey("dim_shipping.shipment_id"),
        nullable=True
    )

    # ============================================================
    # SALES MEASURES
    # ============================================================

    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    unit_price: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    item_revenue: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    item_cost: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    profit: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    # ============================================================
    # ORDER INFORMATION
    # ============================================================

    order_date: Mapped[Optional[Date]] = mapped_column(
        Date,
        nullable=True
    )

    order_status: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True
    )

    shipping_method: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True
    )

    # ============================================================
    # CUSTOMER ATTRIBUTES
    # ============================================================

    customer_signup_date: Mapped[Optional[Date]] = mapped_column(
        Date,
        nullable=True
    )

    gender: Mapped[Optional[str]] = mapped_column(
        String(20),
        nullable=True
    )

    age: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True
    )

    state: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True
    )

    city: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True
    )

    customer_segment: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True
    )

    preferred_device: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True
    )

    preferred_payment_method: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True
    )

    acquisition_channel: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True
    )

    loyalty_tier: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True
    )

    # ============================================================
    # PRODUCT ATTRIBUTES
    # ============================================================

    product_name: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True
    )

    brand: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True
    )

    # ============================================================
    # DISCOUNT
    # ============================================================

    discount_percentage: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True
    )

    # ============================================================
    # PAYMENT INFORMATION
    # ============================================================

    payment_method: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True
    )

    payment_status: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True
    )

    amount_paid: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True
    )

    transaction_fee: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True
    )

    # ============================================================
    # REFUND / RETURN INFORMATION
    # ============================================================

    refund_amount: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.0
    )

    return_id: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True
    )

    return_date: Mapped[Optional[Date]] = mapped_column(
        Date,
        nullable=True
    )

    return_reason: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True
    )

    return_status: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        default="Not Returned"
    )