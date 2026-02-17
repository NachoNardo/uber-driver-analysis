from decimal import Decimal
from typing import List, Optional

from sqlalchemy.orm import Session

from app.db.daos.refill_dao import RefillDAO
from app.models.refill import Refill


class RefillService:
    def __init__(self, session: Session):
        self.dao = RefillDAO(session)

    def create(
        self,
        value: Decimal,
        liters: float,
        current_distance_traveled: float,
    ) -> Refill:
        return self.dao.create(
            value=value,
            liters=liters,
            current_distance_traveled=current_distance_traveled,
        )

    def get_by_id(self, refill_id: int) -> Optional[Refill]:
        return self.dao.get_by_id(refill_id)

    def get_all(self) -> List[Refill]:
        return self.dao.get_all()

    def update(
        self,
        refill_id: int,
        value: Optional[Decimal] = None,
        liters: Optional[float] = None,
        current_distance_traveled: Optional[float] = None,
    ) -> Optional[Refill]:
        return self.dao.update(
            refill_id=refill_id,
            value=value,
            liters=liters,
            current_distance_traveled=current_distance_traveled,
        )

    def delete(self, refill_id: int) -> bool:
        return self.dao.delete(refill_id)

    def search(
        self,
        min_value: Optional[Decimal] = None,
        max_value: Optional[Decimal] = None,
        min_liters: Optional[float] = None,
        max_liters: Optional[float] = None,
        min_distance: Optional[float] = None,
        max_distance: Optional[float] = None,
    ) -> List[Refill]:
        return self.dao.search(
            min_value=min_value,
            max_value=max_value,
            min_liters=min_liters,
            max_liters=max_liters,
            min_distance=min_distance,
            max_distance=max_distance,
        )
