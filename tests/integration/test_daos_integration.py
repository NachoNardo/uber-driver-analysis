from datetime import datetime
from decimal import Decimal
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.daos.travel_dao import TravelDAO
from app.db.daos.refill_dao import RefillDAO
from app.models.base import Base


class DAOIntegrationBase(TestCase):
    def setUp(self):
        self.temp_dir = TemporaryDirectory()
        db_file = Path(self.temp_dir.name) / "test_uber_analysis.db"

        self.engine = create_engine(f"sqlite+pysqlite:///{db_file}")
        self.SessionLocal = sessionmaker(bind=self.engine)

        Base.metadata.create_all(bind=self.engine)
        self.session = self.SessionLocal()

    def tearDown(self):
        self.session.close()
        Base.metadata.drop_all(bind=self.engine)
        self.engine.dispose()
        self.temp_dir.cleanup()


class TestTravelDAOIntegration(DAOIntegrationBase):
    def setUp(self):
        super().setUp()
        self.dao = TravelDAO(self.session)

    def test_crud_flow(self):
        created = self.dao.create(
            total_value=Decimal("30.00"),
            street_start="Alpha",
            neiborghood_start="Centro",
            street_end="Beta",
            neiborghood_end="Sul",
            distance_start=1000.0,
            distance_travel=12.5,
            time_start=datetime(2026, 1, 1, 8, 0),
            time_reach=datetime(2026, 1, 1, 8, 20),
            time_end=datetime(2026, 1, 1, 8, 35),
            time_total=35,
        )

        fetched = self.dao.get_by_id(created.id)
        self.assertIsNotNone(fetched)
        self.assertEqual(Decimal("30.00"), fetched.total_value)

        updated = self.dao.update(created.id, total_value=Decimal("35.00"), street_start="Gamma")
        self.assertIsNotNone(updated)
        self.assertEqual(Decimal("35.00"), updated.total_value)
        self.assertEqual("Gamma", updated.street_start)

        all_items = self.dao.get_all()
        self.assertEqual(1, len(all_items))

        deleted = self.dao.delete(created.id)
        self.assertTrue(deleted)
        self.assertIsNone(self.dao.get_by_id(created.id))

    def test_search_filters(self):
        self.dao.create(
            total_value=Decimal("10.00"),
            street_start="Rua A",
            neiborghood_start="Centro",
            street_end="Rua B",
            neiborghood_end="Norte",
            distance_start=100.0,
            distance_travel=2.0,
            time_start=datetime(2026, 1, 10, 10, 0),
            time_reach=datetime(2026, 1, 10, 10, 5),
            time_end=datetime(2026, 1, 10, 10, 10),
            time_total=10,
        )
        self.dao.create(
            total_value=Decimal("50.00"),
            street_start="Rua C",
            neiborghood_start="Sul",
            street_end="Rua D",
            neiborghood_end="Leste",
            distance_start=200.0,
            distance_travel=8.0,
            time_start=datetime(2026, 1, 11, 11, 0),
            time_reach=datetime(2026, 1, 11, 11, 10),
            time_end=datetime(2026, 1, 11, 11, 25),
            time_total=25,
        )

        result = self.dao.search(
            neiborghood_start="centro",
            min_value=Decimal("9.00"),
            max_value=Decimal("15.00"),
            start_date=datetime(2026, 1, 10, 0, 0),
            end_date=datetime(2026, 1, 10, 23, 59),
        )

        self.assertEqual(1, len(result))
        self.assertEqual("Rua A", result[0].street_start)


class TestRefillDAOIntegration(DAOIntegrationBase):
    def setUp(self):
        super().setUp()
        self.dao = RefillDAO(self.session)

    def test_crud_flow(self):
        created = self.dao.create(
            value=Decimal("120.00"),
            liters=42.0,
            current_distance_traveled=1500.0,
        )

        fetched = self.dao.get_by_id(created.id)
        self.assertIsNotNone(fetched)
        self.assertEqual(Decimal("120.00"), fetched.value)

        updated = self.dao.update(
            created.id,
            value=Decimal("140.00"),
            liters=45.0,
            current_distance_traveled=1700.0,
        )
        self.assertIsNotNone(updated)
        self.assertEqual(Decimal("140.00"), updated.value)
        self.assertEqual(45.0, updated.liters)
        self.assertEqual(1700.0, updated.current_distance_traveled)

        all_items = self.dao.get_all()
        self.assertEqual(1, len(all_items))

        deleted = self.dao.delete(created.id)
        self.assertTrue(deleted)
        self.assertIsNone(self.dao.get_by_id(created.id))

    def test_search_filters(self):
        self.dao.create(value=Decimal("100.00"), liters=40.0, current_distance_traveled=1000.0)
        self.dao.create(value=Decimal("200.00"), liters=50.0, current_distance_traveled=2000.0)

        result = self.dao.search(
            min_value=Decimal("90.00"),
            max_value=Decimal("150.00"),
            min_liters=35.0,
            max_liters=45.0,
            min_distance=900.0,
            max_distance=1500.0,
        )

        self.assertEqual(1, len(result))
        self.assertEqual(Decimal("100.00"), result[0].value)
