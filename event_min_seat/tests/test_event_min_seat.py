# Copyright 2023 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import exceptions
from odoo.tests.common import TransactionCase


class TestEventMinSeat(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.event_type = cls.env["event.type"].create(
            {
                "name": "Test event type",
                "has_seats_limitation": True,
                "default_registration_min": 5,
                "seats_max": 10,
            }
        )
        cls.event = cls.env["event.event"].create(
            {
                "name": "Test event",
                "event_type_id": cls.env.ref("event.event_type_data_ticket").id,
                "date_begin": "2023-01-01",
                "date_end": "2023-01-01",
            }
        )

    def test_event_type_no_has_seats_limitation(self):
        self.event_type.has_seats_limitation = False
        self.assertEqual(self.event_type.default_registration_min, 0)

    def test_event_propagation_from_type(self):
        self.event.event_type_id = self.event_type.id
        self.assertEqual(self.event.seats_min, 5)

    def test_check_seats_min_max(self):
        self.event.write({"seats_max": 5, "seats_limited": True})
        with self.assertRaises(exceptions.ValidationError):
            self.event.seats_min = 6
