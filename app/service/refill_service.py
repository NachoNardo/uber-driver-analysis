from decimal import Decimal
from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.refill import Refill


class RefillService:
    def __init__(self, session: Session):
        self.session = session

    def create(
        self,
        value: Decimal,
        liters: float,
        current_distance_traveled: float
    ) -> Refill:
        refill = Refill(
            value=value,
            liters=liters,
            current_distance_traveled=current_distance_traveled
        )

        self.session.add(refill)
        self.session.commit()
        self.session.refresh(refill)

        return refill

    def get_by_id(self, refill_id: int) -> Optional[Refill]:
        stmt = select(Refill).where(Refill.id == refill_id)
        return self.session.scalars(stmt).first()

    def get_all(self) -> List[Refill]:
        stmt = select(Refill)
        return list(self.session.scalars(stmt).all())

    def update(
        self,
        refill_id: int,
        value: Optional[Decimal] = None,
        liters: Optional[float] = None,
        current_distance_traveled: Optional[float] = None
    ) -> Optional[Refill]:

        refill = self.get_by_id(refill_id)

        if not refill:
            return None

        if value is not None:
            refill.value = value

        if liters is not None:
            refill.liters = liters

        if current_distance_traveled is not None:
            refill.current_distance_traveled = current_distance_traveled

        self.session.commit()
        self.session.refresh(refill)

        return refill

    def delete(self, refill_id: int) -> bool:
        refill = self.get_by_id(refill_id)

        if not refill:
            return False

        self.session.delete(refill)
        self.session.commit()

        return True

    def search(
        self,
        min_value: Optional[Decimal] = None,
        max_value: Optional[Decimal] = None,
        min_liters: Optional[float] = None,
        max_liters: Optional[float] = None,
        min_distance: Optional[float] = None,
        max_distance: Optional[float] = None,
    ) -> List[Refill]:

        stmt = select(Refill)

        if min_value is not None:
            stmt = stmt.where(Refill.value >= min_value)

        if max_value is not None:
            stmt = stmt.where(Refill.value <= max_value)

        if min_liters is not None:
            stmt = stmt.where(Refill.liters >= min_liters)

        if max_liters is not None:
            stmt = stmt.where(Refill.liters <= max_liters)

        if min_distance is not None:
            stmt = stmt.where(
                Refill.current_distance_traveled >= min_distance
            )

        if max_distance is not None:
            stmt = stmt.where(
                Refill.current_distance_traveled <= max_distance
            )

        return list(self.session.scalars(stmt).all())
