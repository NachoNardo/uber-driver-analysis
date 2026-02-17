from datetime import datetime
from decimal import Decimal
from types import SimpleNamespace
from unittest import TestCase
from unittest.mock import Mock

from app.db.daos.travel_dao import TravelDAO


class TestTravelDAOUnit(TestCase):
    def setUp(self):
        self.session = Mock()
        self.dao = TravelDAO(self.session)

    def test_create_adds_and_commits(self):
        travel = self.dao.create(
            total_value=Decimal("12.50"),
            street_start="A",
            neiborghood_start="B",
            street_end="C",
            neiborghood_end="D",
            distance_start=100.0,
            distance_travel=5.0,
            time_start=datetime(2026, 1, 1, 10, 0),
            time_reach=datetime(2026, 1, 1, 10, 10),
            time_end=datetime(2026, 1, 1, 10, 20),
            time_total=20,
        )

        self.session.add.assert_called_once_with(travel)
        self.session.commit.assert_called_once()
        self.session.refresh.assert_called_once_with(travel)

    def test_update_returns_none_when_not_found(self):
        self.dao.get_by_id = Mock(return_value=None)

        result = self.dao.update(1, street_start="X")

        self.assertIsNone(result)
        self.session.commit.assert_not_called()
        self.session.refresh.assert_not_called()

    def test_update_changes_attributes_and_commits(self):
        travel = SimpleNamespace(street_start="Old", total_value=Decimal("10.00"))
        self.dao.get_by_id = Mock(return_value=travel)

        result = self.dao.update(1, street_start="New", total_value=Decimal("20.00"))

        self.assertIs(result, travel)
        self.assertEqual("New", travel.street_start)
        self.assertEqual(Decimal("20.00"), travel.total_value)
        self.session.commit.assert_called_once()
        self.session.refresh.assert_called_once_with(travel)

    def test_delete_returns_false_when_not_found(self):
        self.dao.get_by_id = Mock(return_value=None)

        deleted = self.dao.delete(999)

        self.assertFalse(deleted)
        self.session.delete.assert_not_called()
        self.session.commit.assert_not_called()

    def test_delete_removes_entity_when_found(self):
        travel = SimpleNamespace(id=1)
        self.dao.get_by_id = Mock(return_value=travel)

        deleted = self.dao.delete(1)

        self.assertTrue(deleted)
        self.session.delete.assert_called_once_with(travel)
        self.session.commit.assert_called_once()
