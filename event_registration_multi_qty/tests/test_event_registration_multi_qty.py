# Copyright 2017 Sergio Teruel<sergio.teruel@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.exceptions import ValidationError
from odoo.tests import common


class EventRegistrationMultiQty(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.event = cls.env["event.event"].create(
            {
                "name": "Test event",
                "date_begin": "2017-05-26 20:00:00",
                "date_end": "2017-05-30 22:00:00",
                "registration_multi_qty": True,
            }
        )
        cls.attendee_draft = cls.env["event.registration"].create(
            {
                "name": "Test attendee draft",
                "event_id": cls.event.id,
                "state": "draft",
                "qty": 5,
            }
        )
        cls.attendee_open = cls.env["event.registration"].create(
            {
                "name": "Test attendee done",
                "event_id": cls.event.id,
                "state": "open",
                "qty": 10,
            }
        )
        cls.attendee_open_other = cls.env["event.registration"].create(
            {
                "name": "Test attendee done",
                "event_id": cls.event.id,
                "state": "open",
                "qty": 10,
            }
        )
        cls.attendee_done = cls.env["event.registration"].create(
            {"name": "Test attendee done", "event_id": cls.event.id, "state": "done"}
        )
        cls.event_no_qty_option = cls.env["event.event"].create(
            {
                "name": "Test event2",
                "date_begin": "2017-05-26 20:00:00",
                "date_end": "2017-05-30 22:00:00",
                "registration_multi_qty": False,
            }
        )
        cls.attendee_no_qty_done = cls.env["event.registration"].create(
            {
                "name": "Test attendee done",
                "event_id": cls.event_no_qty_option.id,
                "state": "done",
            }
        )

    def test_compute_seats(self):
        self.assertEqual(self.event.seats_unconfirmed, 5)
        self.assertEqual(self.event.seats_reserved, 20)
        self.assertEqual(self.event.seats_used, 1)

    def test_change_event_option(self):
        with self.assertRaises(ValidationError):
            self.event.registration_multi_qty = False

    def test_registration_qty(self):
        with self.assertRaises(ValidationError):
            self.attendee_no_qty_done.qty = 15
