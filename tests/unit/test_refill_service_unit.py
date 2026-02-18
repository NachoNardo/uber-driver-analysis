from decimal import Decimal
from unittest import TestCase
from unittest.mock import Mock, patch

from app.service.refill_service import RefillService


class TestRefillServiceUnit(TestCase):
    @patch("app.service.refill_service.RefillDAO")
    def test_init_creates_dao_with_session(self, dao_cls):
        session = Mock()

        service = RefillService(session)

        dao_cls.assert_called_once_with(session)
        self.assertIs(service.dao, dao_cls.return_value)

    @patch("app.service.refill_service.RefillDAO")
    def test_create_delegates_to_dao(self, dao_cls):
        session = Mock()
        dao = dao_cls.return_value
        expected = object()
        dao.create.return_value = expected

        service = RefillService(session)
        result = service.create(
            value=Decimal("120.00"),
            liters=42.0,
            current_distance_traveled=1400.0,
        )

        dao.create.assert_called_once_with(
            value=Decimal("120.00"),
            liters=42.0,
            current_distance_traveled=1400.0,
        )
        self.assertIs(result, expected)

    @patch("app.service.refill_service.RefillDAO")
    def test_get_by_id_delegates_to_dao(self, dao_cls):
        session = Mock()
        dao = dao_cls.return_value
        dao.get_by_id.return_value = object()
        service = RefillService(session)

        result = service.get_by_id(11)

        dao.get_by_id.assert_called_once_with(11)
        self.assertIs(result, dao.get_by_id.return_value)

    @patch("app.service.refill_service.RefillDAO")
    def test_get_all_delegates_to_dao(self, dao_cls):
        session = Mock()
        dao = dao_cls.return_value
        dao.get_all.return_value = [object()]
        service = RefillService(session)

        result = service.get_all()

        dao.get_all.assert_called_once_with()
        self.assertIs(result, dao.get_all.return_value)

    @patch("app.service.refill_service.RefillDAO")
    def test_update_delegates_to_dao(self, dao_cls):
        session = Mock()
        dao = dao_cls.return_value
        dao.update.return_value = object()
        service = RefillService(session)

        result = service.update(
            2,
            value=Decimal("130.00"),
            liters=44.0,
            current_distance_traveled=1600.0,
        )

        dao.update.assert_called_once_with(
            refill_id=2,
            value=Decimal("130.00"),
            liters=44.0,
            current_distance_traveled=1600.0,
        )
        self.assertIs(result, dao.update.return_value)

    @patch("app.service.refill_service.RefillDAO")
    def test_delete_delegates_to_dao(self, dao_cls):
        session = Mock()
        dao = dao_cls.return_value
        dao.delete.return_value = True
        service = RefillService(session)

        result = service.delete(4)

        dao.delete.assert_called_once_with(4)
        self.assertTrue(result)

    @patch("app.service.refill_service.RefillDAO")
    def test_search_delegates_to_dao(self, dao_cls):
        session = Mock()
        dao = dao_cls.return_value
        dao.search.return_value = [object()]
        service = RefillService(session)

        result = service.search(
            min_value=Decimal("80.00"),
            max_value=Decimal("150.00"),
            min_liters=35.0,
            max_liters=50.0,
            min_distance=900.0,
            max_distance=2000.0,
        )

        dao.search.assert_called_once_with(
            min_value=Decimal("80.00"),
            max_value=Decimal("150.00"),
            min_liters=35.0,
            max_liters=50.0,
            min_distance=900.0,
            max_distance=2000.0,
        )
        self.assertIs(result, dao.search.return_value)
