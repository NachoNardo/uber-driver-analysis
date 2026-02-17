from decimal import Decimal

from sqlalchemy import Float, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Refill(Base):
    __tablename__ = "refills"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    value: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    liters: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    current_distance_traveled: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
