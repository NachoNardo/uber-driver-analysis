from datetime import datetime
from decimal import Decimal
from sqlalchemy import String, Numeric, Float, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column

from base import Base


class Travel(Base):
    __tablename__ = "travels"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    total_value: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False
    )

    street_start: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    neiborghood_start: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    street_end: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    neiborghood_end: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    distance_start: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    distance_travel: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    time_start: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    time_reach: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    time_end: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    time_total: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )
from datetime import datetime
from decimal import Decimal
from sqlalchemy import String, Numeric, Float, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Travel(Base):
    __tablename__ = "travels"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    total_value: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False
    )

    street_start: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    neiborghood_start: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    street_end: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    neiborghood_end: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    distance_start: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    distance_travel: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    time_start: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    time_reach: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    time_end: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    time_total: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )
