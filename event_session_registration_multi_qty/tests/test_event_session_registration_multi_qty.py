# Copyright 2017-19 Tecnativa - David Vidal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0).
from freezegun import freeze_time

from odoo.tests import common


@freeze_time("2023-06-01 09:00:00", tick=True)
class EventSessionRegistrationMultiQty(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.mail_template_reminder = cls.env.ref("event_session.event_session_reminder")
        cls.event = cls.env["event.event"].create(
            {
                "name": "Test event",
                "date_begin": "2017-05-26 20:00:00",
                "date_end": "2017-05-30 22:00:00",
                "seats_limited": True,
                "seats_max": "250",
                "registration_multi_qty": True,
            }
        )
        cls.session = cls.env["event.session"].create(
            {
                "date_begin": "2017-05-26 20:00:00",
                "date_end": "2017-05-26 22:00:00",
                "event_id": cls.event.id,
                "seats_limited": cls.event.seats_limited,
                "seats_max": cls.event.seats_max,
            }
        )
        cls.attendee_draft = cls.env["event.registration"].create(
            {
                "name": "Test attendee draft",
                "event_id": cls.event.id,
                "session_id": cls.session.id,
                "qty": 5,
            }
        )
        cls.attendee_open = cls.env["event.registration"].create(
            {
                "name": "Test attendee open",
                "event_id": cls.event.id,
                "session_id": cls.session.id,
                "qty": 20,
            }
        )
        cls.attendee_done = cls.env["event.registration"].create(
            {
                "name": "Test attendee done",
                "event_id": cls.event.id,
                "session_id": cls.session.id,
                "qty": 1,
            }
        )
        cls.attendee_cancel = cls.env["event.registration"].create(
            {
                "name": "Test attendee cancel",
                "event_id": cls.event.id,
                "session_id": cls.session.id,
                "qty": 10,
            }
        )
        cls.wizard = cls.env["wizard.event.session"].create(
            {
                "event_id": cls.event.id,
                "mon": True,
                "tue": True,
                "wed": True,
                "thu": True,
                "fri": True,
                "sat": True,
                "sun": True,
                "duration": 2,
                "start": "2023-06-07 09:00:00",
                "until": "2023-06-15 09:00:00",
            }
        )
        cls.event_mail = cls.env["event.mail"].create(
            {
                "event_id": cls.event.id,
                "interval_nbr": 15,
                "interval_unit": "days",
                "interval_type": "before_event",
                "template_ref": f"mail.template,{cls.mail_template_reminder.id}",
            }
        )

    def test_compute_seats(self):
        self.attendee_open.state = "open"
        self.attendee_draft.state = "draft"
        self.attendee_done.state = "done"
        self.attendee_cancel.state = "cancel"
        self.assertEqual(self.session.seats_unconfirmed, 5)
        self.assertEqual(self.session.seats_reserved, 20)
        self.assertEqual(self.session.seats_used, 1)
        self.assertEqual(self.session.seats_expected, 26)
        self.assertEqual(self.session.seats_available, 229)
        self.attendee_cancel.state = "draft"
        self.assertEqual(self.session.seats_unconfirmed, 15)
        self.assertEqual(self.session.seats_expected, 36)
        self.assertEqual(self.session.seats_available, 229)
        self.attendee_cancel.state = "open"
        self.assertEqual(self.session.seats_unconfirmed, 5)
        self.assertEqual(self.session.seats_expected, 36)
        self.assertEqual(self.session.seats_available, 219)
