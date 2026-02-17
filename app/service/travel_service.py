from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from sqlalchemy.orm import Session

from app.db.daos.travel_dao import TravelDAO
from app.models.travel import Travel


class TravelService:
    def __init__(self, session: Session):
        self.dao = TravelDAO(session)

    def create(
        self,
        total_value: Decimal,
        street_start: str,
        neiborghood_start: str,
        street_end: str,
        neiborghood_end: str,
        distance_start: float,
        distance_travel: float,
        time_start: datetime,
        time_reach: datetime,
        time_end: datetime,
        time_total: int,
    ) -> Travel:
        return self.dao.create(
            total_value=total_value,
            street_start=street_start,
            neiborghood_start=neiborghood_start,
            street_end=street_end,
            neiborghood_end=neiborghood_end,
            distance_start=distance_start,
            distance_travel=distance_travel,
            time_start=time_start,
            time_reach=time_reach,
            time_end=time_end,
            time_total=time_total,
        )

    def get_by_id(self, travel_id: int) -> Optional[Travel]:
        return self.dao.get_by_id(travel_id)

    def get_all(self) -> List[Travel]:
        return self.dao.get_all()

    def update(self, travel_id: int, **kwargs) -> Optional[Travel]:
        return self.dao.update(travel_id, **kwargs)

    def delete(self, travel_id: int) -> bool:
        return self.dao.delete(travel_id)

    def search(
        self,
        street_start: Optional[str] = None,
        neiborghood_start: Optional[str] = None,
        street_end: Optional[str] = None,
        neiborghood_end: Optional[str] = None,
        min_value: Optional[Decimal] = None,
        max_value: Optional[Decimal] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> List[Travel]:
        return self.dao.search(
            street_start=street_start,
            neiborghood_start=neiborghood_start,
            street_end=street_end,
            neiborghood_end=neiborghood_end,
            min_value=min_value,
            max_value=max_value,
            start_date=start_date,
            end_date=end_date,
        )
