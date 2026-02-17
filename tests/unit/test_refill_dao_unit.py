from decimal import Decimal
from types import SimpleNamespace
from unittest import TestCase
from unittest.mock import Mock

from app.db.daos.refill_dao import RefillDAO


class TestRefillDAOUnit(TestCase):
    def setUp(self):
        self.session = Mock()
        self.dao = RefillDAO(self.session)

    def test_create_adds_and_commits(self):
        refill = self.dao.create(
            value=Decimal("100.00"),
            liters=40.0,
            current_distance_traveled=1200.0,
        )

        self.session.add.assert_called_once_with(refill)
        self.session.commit.assert_called_once()
        self.session.refresh.assert_called_once_with(refill)

    def test_update_returns_none_when_not_found(self):
        self.dao.get_by_id = Mock(return_value=None)

        result = self.dao.update(1, value=Decimal("150.00"))

        self.assertIsNone(result)
        self.session.commit.assert_not_called()
        self.session.refresh.assert_not_called()

    def test_update_changes_attributes_and_commits(self):
        refill = SimpleNamespace(
            value=Decimal("100.00"),
            liters=40.0,
            current_distance_traveled=1200.0,
        )
        self.dao.get_by_id = Mock(return_value=refill)

        result = self.dao.update(
            1,
            value=Decimal("150.00"),
            liters=45.0,
            current_distance_traveled=1500.0,
        )

        self.assertIs(result, refill)
        self.assertEqual(Decimal("150.00"), refill.value)
        self.assertEqual(45.0, refill.liters)
        self.assertEqual(1500.0, refill.current_distance_traveled)
        self.session.commit.assert_called_once()
        self.session.refresh.assert_called_once_with(refill)

    def test_delete_returns_false_when_not_found(self):
        self.dao.get_by_id = Mock(return_value=None)

        deleted = self.dao.delete(999)

        self.assertFalse(deleted)
        self.session.delete.assert_not_called()
        self.session.commit.assert_not_called()

    def test_delete_removes_entity_when_found(self):
        refill = SimpleNamespace(id=1)
        self.dao.get_by_id = Mock(return_value=refill)

        deleted = self.dao.delete(1)

        self.assertTrue(deleted)
        self.session.delete.assert_called_once_with(refill)
        self.session.commit.assert_called_once()
