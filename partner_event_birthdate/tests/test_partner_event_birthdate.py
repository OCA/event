# Copyright 2026 INVITU (<https://www.invitu.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from datetime import date, datetime

from odoo.tests import Form
from odoo.tests.common import TransactionCase


class TestPartnerEventBirthdate(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.event = cls.env["event.event"].create(
            {
                "name": "Test Event",
                "date_begin": datetime(2026, 9, 1, 8, 0),
                "date_end": datetime(2026, 9, 1, 18, 0),
                "create_partner": True,
            }
        )
        cls.partner = cls.env["res.partner"].create(
            {"name": "Jane Smith", "birthdate_date": date(2010, 3, 15)}
        )

    def _new_reg(self, vals):
        vals["event_id"] = self.event.id
        return self.env["event.registration"].create(vals)

    def test_birthdate_date_field_on_registration(self):
        """birthdate_date is correctly stored on registration."""
        reg = self._new_reg({"name": "John Smith", "birthdate_date": date(2010, 3, 15)})
        self.assertEqual(reg.birthdate_date, date(2010, 3, 15))

    def test_prepare_partner_passes_birthdate_date(self):
        """_prepare_partner includes birthdate_date."""
        reg = self._new_reg({"name": "John Smith", "birthdate_date": date(2010, 3, 15)})
        vals = reg._prepare_partner({"birthdate_date": reg.birthdate_date})
        self.assertEqual(vals["birthdate_date"], date(2010, 3, 15))

    def test_onchange_partner_id_syncs_birthdate_date(self):
        """birthdate is synced from attendee_partner_id with _onchange"""
        reg_form = Form(self.env["event.registration"])
        reg_form.event_id = self.event
        reg_form.attendee_partner_id = self.partner
        reg = reg_form.save()
        self.assertEqual(reg.birthdate_date, date(2010, 3, 15))
