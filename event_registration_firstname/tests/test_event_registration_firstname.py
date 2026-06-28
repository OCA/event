# Copyright 2026 INVITU (<https://www.invitu.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from datetime import datetime

from odoo.tests.common import TransactionCase


class TestEventRegistrationFirstname(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.event = cls.env["event.event"].create(
            {
                "name": "Test Event",
                "date_begin": datetime(2026, 9, 1, 8, 0),
                "date_end": datetime(2026, 9, 1, 18, 0),
            }
        )

    def _new_reg(self, vals):
        vals["event_id"] = self.event.id
        return self.env["event.registration"].create(vals)

    def _set_order(self, order):
        self.env["ir.config_parameter"].sudo().set_param("partner_names_order", order)

    def test_create_from_firstname_lastname_last_first(self):
        """firstname + lastname → name computed in last_first order."""
        self._set_order("last_first")
        reg = self._new_reg({"firstname": "John", "lastname": "Smith"})
        self.assertEqual(reg.name, "Smith John")

    def test_create_from_firstname_lastname_first_last(self):
        """firstname + lastname → name computed in first_last order."""
        self._set_order("first_last")
        reg = self._new_reg({"firstname": "John", "lastname": "Smith"})
        self.assertEqual(reg.name, "John Smith")

    def test_create_from_name_splits(self):
        """name only → split into firstname + lastname per configured order."""
        self._set_order("last_first")
        reg = self._new_reg({"name": "Smith John"})
        self.assertEqual(reg.lastname, "Smith")
        self.assertEqual(reg.firstname, "John")

    def test_write_firstname_updates_name(self):
        """Updating firstname recomputes name."""
        self._set_order("last_first")
        reg = self._new_reg({"firstname": "John", "lastname": "Smith"})
        reg.write({"firstname": "Peter"})
        self.assertEqual(reg.name, "Smith Peter")
