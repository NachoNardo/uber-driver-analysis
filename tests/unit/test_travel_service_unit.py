from datetime import datetime
from decimal import Decimal
from unittest import TestCase
from unittest.mock import Mock, patch

from app.service.travel_service import TravelService


class TestTravelServiceUnit(TestCase):
    @patch("app.service.travel_service.TravelDAO")
    def test_init_creates_dao_with_session(self, dao_cls):
        session = Mock()

        service = TravelService(session)

        dao_cls.assert_called_once_with(session)
        self.assertIs(service.dao, dao_cls.return_value)

    @patch("app.service.travel_service.TravelDAO")
    def test_create_delegates_to_dao(self, dao_cls):
        session = Mock()
        dao = dao_cls.return_value
        expected = object()
        dao.create.return_value = expected

        service = TravelService(session)
        result = service.create(
            total_value=Decimal("25.50"),
            street_start="A",
            neiborghood_start="Centro",
            street_end="B",
            neiborghood_end="Sul",
            distance_start=100.0,
            distance_travel=8.5,
            time_start=datetime(2026, 1, 1, 10, 0),
            time_reach=datetime(2026, 1, 1, 10, 10),
            time_end=datetime(2026, 1, 1, 10, 20),
            time_total=20,
        )

        dao.create.assert_called_once_with(
            total_value=Decimal("25.50"),
            street_start="A",
            neiborghood_start="Centro",
            street_end="B",
            neiborghood_end="Sul",
            distance_start=100.0,
            distance_travel=8.5,
            time_start=datetime(2026, 1, 1, 10, 0),
            time_reach=datetime(2026, 1, 1, 10, 10),
            time_end=datetime(2026, 1, 1, 10, 20),
            time_total=20,
        )
        self.assertIs(result, expected)

    @patch("app.service.travel_service.TravelDAO")
    def test_get_by_id_delegates_to_dao(self, dao_cls):
        session = Mock()
        dao = dao_cls.return_value
        dao.get_by_id.return_value = object()
        service = TravelService(session)

        result = service.get_by_id(7)

        dao.get_by_id.assert_called_once_with(7)
        self.assertIs(result, dao.get_by_id.return_value)

    @patch("app.service.travel_service.TravelDAO")
    def test_get_all_delegates_to_dao(self, dao_cls):
        session = Mock()
        dao = dao_cls.return_value
        dao.get_all.return_value = [object()]
        service = TravelService(session)

        result = service.get_all()

        dao.get_all.assert_called_once_with()
        self.assertIs(result, dao.get_all.return_value)

    @patch("app.service.travel_service.TravelDAO")
    def test_update_delegates_to_dao(self, dao_cls):
        session = Mock()
        dao = dao_cls.return_value
        dao.update.return_value = object()
        service = TravelService(session)

        result = service.update(1, street_start="Nova", total_value=Decimal("33.00"))

        dao.update.assert_called_once_with(1, street_start="Nova", total_value=Decimal("33.00"))
        self.assertIs(result, dao.update.return_value)

    @patch("app.service.travel_service.TravelDAO")
    def test_delete_delegates_to_dao(self, dao_cls):
        session = Mock()
        dao = dao_cls.return_value
        dao.delete.return_value = True
        service = TravelService(session)

        result = service.delete(3)

        dao.delete.assert_called_once_with(3)
        self.assertTrue(result)

    @patch("app.service.travel_service.TravelDAO")
    def test_search_delegates_to_dao(self, dao_cls):
        session = Mock()
        dao = dao_cls.return_value
        dao.search.return_value = [object()]
        service = TravelService(session)

        result = service.search(
            street_start="Rua",
            neiborghood_start="Centro",
            street_end="Av",
            neiborghood_end="Norte",
            min_value=Decimal("10.00"),
            max_value=Decimal("100.00"),
            start_date=datetime(2026, 1, 1, 0, 0),
            end_date=datetime(2026, 1, 31, 23, 59),
        )

        dao.search.assert_called_once_with(
            street_start="Rua",
            neiborghood_start="Centro",
            street_end="Av",
            neiborghood_end="Norte",
            min_value=Decimal("10.00"),
            max_value=Decimal("100.00"),
            start_date=datetime(2026, 1, 1, 0, 0),
            end_date=datetime(2026, 1, 31, 23, 59),
        )
        self.assertIs(result, dao.search.return_value)
