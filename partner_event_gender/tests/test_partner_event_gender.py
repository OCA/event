# Copyright 2026 INVITU (<https://www.invitu.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from datetime import datetime

from odoo.tests import Form
from odoo.tests.common import TransactionCase


class TestPartnerEventGender(TransactionCase):
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
            {"name": "Jane Smith", "gender": "female"}
        )

    def _new_reg(self, vals):
        vals["event_id"] = self.event.id
        return self.env["event.registration"].create(vals)

    def test_gender_field_on_registration(self):
        """gender field is correctly stored on registration."""
        reg = self._new_reg({"name": "John Smith", "gender": "male"})
        self.assertEqual(reg.gender, "male")

    def test_prepare_partner_passes_gender(self):
        """_prepare_partner includes gender."""
        reg = self._new_reg({"name": "Jane Smith", "gender": "female"})
        vals = reg._prepare_partner({"gender": reg.gender})
        self.assertEqual(vals["gender"], "female")

    def test_onchange_partner_id_syncs_gender(self):
        """gender is synced from attendee_partner_id via _onchange_partner_id."""
        reg_form = Form(self.env["event.registration"])
        reg_form.event_id = self.event
        reg_form.attendee_partner_id = self.partner
        reg = reg_form.save()
        self.assertEqual(reg.gender, "female")
