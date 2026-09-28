from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from DB.db_config import Base


class DimShipping(Base):
    __tablename__ = "dim_shipping"

    shipment_id: Mapped[str] = mapped_column(
        String(20),
        primary_key=True
    )

    shipping_method: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    warehouse_city: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    delivery_city: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )