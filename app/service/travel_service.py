from typing import List, Optional
from datetime import datetime
from decimal import Decimal

from sqlalchemy.orm import Session
from sqlalchemy import select, and_

from app.models.travel import Travel


class TravelService:
    def __init__(self, session: Session):
        self.session = session

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
        time_total: int
    ) -> Travel:

        travel = Travel(
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
            time_total=time_total
        )

        self.session.add(travel)
        self.session.commit()
        self.session.refresh(travel)

        return travel

    def get_by_id(self, travel_id: int) -> Optional[Travel]:
        stmt = select(Travel).where(Travel.id == travel_id)
        result = self.session.execute(stmt).scalar_one_or_none()
        return result

    def get_all(self) -> List[Travel]:
        stmt = select(Travel)
        result = self.session.execute(stmt).scalars().all()
        return result

    def update(self, travel_id: int, **kwargs) -> Optional[Travel]:
        travel = self.get_by_id(travel_id)

        if not travel:
            return None

        for key, value in kwargs.items():
            if hasattr(travel, key):
                setattr(travel, key, value)

        self.session.commit()
        self.session.refresh(travel)

        return travel

    def delete(self, travel_id: int) -> bool:
        travel = self.get_by_id(travel_id)

        if not travel:
            return False

        self.session.delete(travel)
        self.session.commit()

        return True

    def search(
        self,
        street_start: Optional[str] = None,
        neiborghood_start: Optional[str] = None,
        street_end: Optional[str] = None,
        neiborghood_end: Optional[str] = None,
        min_value: Optional[Decimal] = None,
        max_value: Optional[Decimal] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Travel]:

        filters = []

        if street_start:
            filters.append(Travel.street_start.ilike(f"%{street_start}%"))

        if neiborghood_start:
            filters.append(Travel.neiborghood_start.ilike(f"%{neiborghood_start}%"))

        if street_end:
            filters.append(Travel.street_end.ilike(f"%{street_end}%"))

        if neiborghood_end:
            filters.append(Travel.neiborghood_end.ilike(f"%{neiborghood_end}%"))

        if min_value is not None:
            filters.append(Travel.total_value >= min_value)

        if max_value is not None:
            filters.append(Travel.total_value <= max_value)

        if start_date is not None:
            filters.append(Travel.time_start >= start_date)

        if end_date is not None:
            filters.append(Travel.time_end <= end_date)

        stmt = select(Travel)

        if filters:
            stmt = stmt.where(and_(*filters))

        result = self.session.execute(stmt).scalars().all()

        return result
