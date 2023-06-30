# Copyright 2017-19 Tecnativa - David Vidal
# Copyright 2017 Tecnativa - Pedro M. Baeza
# Copyright 2021 Moka Tourisme (https://www.mokatourisme.fr).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).

from datetime import timedelta

from freezegun import freeze_time

from odoo import fields
from odoo.exceptions import ValidationError
from odoo.tests.common import Form
from odoo.tools import mute_logger

from .common import CommonEventSessionCase


class TestEventSession(CommonEventSessionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.event = cls.env["event.event"].create(
            {
                "name": "Test event",
                "use_sessions": True,
                "seats_limited": True,
                "seats_max": 5,
            }
        )
        cls.session = cls.env["event.session"].create(
            {
                "date_begin": "2017-05-26 20:00:00",
                "date_end": "2017-05-26 21:00:00",
                "event_id": cls.event.id,
            }
        )

    def test_session_name_get(self):
        # Case 1: Same tz than user
        name = self.session.name_get()[0][1]
        self.assertEqual(name, "Test event, May 26, 2017, 10:00:00 PM")
        # Case 2: Different timezone
        self.event.date_tz = "UTC"
        name = self.session.name_get()[0][1]
        self.assertEqual(name, "Test event, May 26, 2017, 8:00:00 PM (UTC)")

    def test_check_dates(self):
        with self.assertRaisesRegex(
            ValidationError,
            "The closing date cannot be earlier than the beginning date",
        ):
            self.session.date_end = "2017-05-26 19:00:00"

    def test_open_registrations(self):
        domain = self.session.action_open_registrations()["domain"]
        attendees = self.env["event.registration"].search(domain)
        self.assertEqual(attendees, self.session.registration_ids)

    def test_event_registration_event_begin_end_dates(self):
        """Test that the date_begin and date_end are set to the session's"""
        # Case 1: Even with sessions
        registration = self.env["event.registration"].create(
            {
                "name": "Test attendee",
                "event_id": self.event.id,
                "session_id": self.session.id,
            }
        )
        self.assertEqual(registration.event_begin_date, self.session.date_begin)
        self.assertEqual(registration.event_end_date, self.session.date_end)
        # Case 2: Regular events
        event = self.env.ref("event.event_0")
        registration = self.env["event.registration"].create(
            {
                "name": "Test attendee",
                "event_id": event.id,
            }
        )
        self.assertEqual(registration.event_begin_date, event.date_begin)
        self.assertEqual(registration.event_end_date, event.date_end)

    def test_event_session_dates_located(self):
        self.session.date_tz = "Europe/Paris"
        self.assertEqual(self.session.date_begin_located, "May 26, 2017, 10:00:00 PM")
        self.assertEqual(self.session.date_end_located, "May 26, 2017, 11:00:00 PM")
        self.session.date_tz = "US/Pacific"
        self.assertEqual(self.session.date_begin_located, "May 26, 2017, 1:00:00 PM")
        self.assertEqual(self.session.date_end_located, "May 26, 2017, 2:00:00 PM")

    def test_event_event_sync_from_event_type(self):
        """Test that the event.type fields are synced to the event.event"""
        event_type = self.env["event.type"].create(
            {
                "name": "Test event type",
                "use_sessions": True,
            }
        )
        event = self.env["event.event"].create(
            {
                "name": "Test event",
                "event_type_id": event_type.id,
                "date_begin": self.event.date_begin,
                "date_end": self.event.date_end,
            }
        )
        self.assertEqual(event.use_sessions, True)

    def test_event_session_form(self):
        # Test workaround for this Odoo bug: https://github.com/odoo/odoo/pull/91373
        session_form = Form(
            self.env["event.session"].with_context(
                default_event_id=self.event.id,
            )
        )
        self.assertEqual(session_form.event_id, self.event)
        self.assertEqual(session_form.name, self.event.name)

    def test_event_event_use_sessions_switch(self):
        # Case 1: We can't change an event to use_sessions after registrations
        event = self.env["event.event"].create(
            {
                "name": "Test event",
                "date_begin": self.event.date_begin,
                "date_end": self.event.date_end,
            }
        )
        self.env["event.registration"].create(
            {
                "event_id": event.id,
                "name": "Test attendee",
            }
        )
        msg = "You can't enable/disable sessions on events with registrations."
        with self.assertRaisesRegex(ValidationError, msg):
            event.use_sessions = True
        # Case 2: We can change it back, if we have no registrations
        # In fact event.sessions are removed when doing so
        self.event.use_sessions = False
        self.assertFalse(self.session.exists())

    @mute_logger("odoo.models.unlink")
    def test_event_event_sessions_count(self):
        """Test that the sessions count is computed correctly"""
        self.assertEqual(self.event.session_count, 1)
        self.session.unlink()
        self.assertEqual(self.event.session_count, 0)

    def test_event_message_subscribe_organizer(self):
        """Test that the organizer is subscribed to the sessions"""
        organizer = self.env["res.partner"].create({"name": "Test organizer"})
        # Case 1: Updating the event's organizer
        self.event.organizer_id = organizer
        self.assertIn(organizer, self.session.message_partner_ids)
        # Case 2: Creating new sessions
        session = self.env["event.session"].create(
            {
                "date_begin": "2017-05-27 20:00:00",
                "date_end": "2017-05-27 21:00:00",
                "event_id": self.event.id,
            }
        )
        self.assertIn(organizer, session.message_partner_ids)

    def test_session_seats(self):
        """Test event session seats constraints"""
        self.assertEqual(self.event.seats_unconfirmed, self.session.seats_unconfirmed)
        self.assertEqual(self.event.seats_used, self.session.seats_used)
        vals = {
            "name": "Test Attendee",
            "event_id": self.event.id,
            "session_id": self.session.id,
            "state": "open",
        }
        # Fill the event session with attendees
        self.env["event.registration"].create([vals] * self.session.seats_available)
        # Try to create another one
        with self.assertRaisesRegex(
            ValidationError, r"There are not enough seats available for:"
        ), self.cr.savepoint():
            self.env["event.registration"].create(vals)
        # Attempt to create a draft registration on a full session
        with self.assertRaisesRegex(
            ValidationError, "No more seats available for this session."
        ), self.cr.savepoint():
            self.env["event.registration"].create(dict(vals, state="draft"))
        # Temporarily allow to create a draft registration and attempt to confirm it
        self.event.seats_limited = False
        registration = self.env["event.registration"].create(dict(vals, state="draft"))
        self.event.seats_limited = True
        with self.assertRaisesRegex(
            ValidationError, r"There are not enough seats available for:"
        ), self.cr.savepoint():
            registration.action_confirm()
            registration.flush_recordset()

    def test_event_seats(self):
        """Test that event.event seats constraints do not apply to sessions"""
        # Case: Event has a limit of 5 seats, but it should apply per-session
        self.event.seats_max = 5
        self.event.seats_limited = True
        # Fill session with attendees
        vals = {
            "name": "Test Attendee",
            "event_id": self.event.id,
            "session_id": self.session.id,
            "state": "open",
        }
        self.assertFalse(self.session.event_registrations_sold_out)
        self.env["event.registration"].create([vals] * 5)
        self.assertTrue(self.session.event_registrations_sold_out)
        # Create a second session and fill it too
        session2 = self.session.copy({})
        vals["session_id"] = session2.id
        self.env["event.registration"].create([vals] * 5)
        # Now attempt to move one registration to another session
        with self.assertRaisesRegex(
            ValidationError, r"There are not enough seats available for:"
        ), self.cr.savepoint():
            self.session.registration_ids[0].session_id = session2
        # Attempt to decrease the event seats limit below the existing registrations
        with self.assertRaisesRegex(
            ValidationError, r"There are not enough seats available for:"
        ), self.cr.savepoint():
            self.event.seats_max = 2
            self.event.flush_recordset()

    def test_session_seats_count(self):
        session_1, session_2 = self.env["event.session"].create(
            [
                {
                    "event_id": self.event.id,
                    "date_begin": fields.Datetime.now(),
                    "date_end": fields.Datetime.now() + timedelta(hours=1),
                },
                {
                    "event_id": self.event.id,
                    "date_begin": fields.Datetime.now() + timedelta(days=1),
                    "date_end": fields.Datetime.now() + timedelta(days=1, hours=1),
                },
            ]
        )
        attendee_1, attendee_2, attendee_3 = self.env["event.registration"].create(
            [
                {
                    "name": "S1: First Atendee",
                    "event_id": self.event.id,
                    "session_id": session_1.id,
                },
                {
                    "name": "S1: Second Atendee",
                    "event_id": self.event.id,
                    "session_id": session_1.id,
                },
                {
                    "name": "S2: First Atendee",
                    "event_id": self.event.id,
                    "session_id": session_2.id,
                },
            ]
        )
        self.assertEqual(session_1.seats_unconfirmed, 2)
        self.assertEqual(session_1.seats_reserved, 0)
        self.assertEqual(session_1.seats_expected, 2)
        self.assertEqual(session_2.seats_unconfirmed, 1)
        self.assertEqual(session_2.seats_reserved, 0)
        self.assertEqual(session_2.seats_expected, 1)
        self.assertEqual(self.event.seats_unconfirmed, 3)
        self.assertEqual(self.event.seats_reserved, 0)
        self.assertEqual(self.event.seats_expected, 3)
        attendee_1.action_confirm()
        self.assertEqual(session_1.seats_unconfirmed, 1)
        self.assertEqual(session_1.seats_reserved, 1)
        self.assertEqual(session_2.seats_unconfirmed, 1)
        self.assertEqual(session_2.seats_reserved, 0)
        self.assertEqual(self.event.seats_unconfirmed, 2)
        self.assertEqual(self.event.seats_reserved, 1)
        attendee_2.action_confirm()
        self.assertEqual(session_1.seats_unconfirmed, 0)
        self.assertEqual(session_1.seats_reserved, 2)
        self.assertEqual(session_2.seats_unconfirmed, 1)
        self.assertEqual(session_2.seats_reserved, 0)
        self.assertEqual(self.event.seats_unconfirmed, 1)
        self.assertEqual(self.event.seats_reserved, 2)
        attendee_3.action_confirm()
        self.assertEqual(session_1.seats_unconfirmed, 0)
        self.assertEqual(session_1.seats_reserved, 2)
        self.assertEqual(session_2.seats_unconfirmed, 0)
        self.assertEqual(session_2.seats_reserved, 1)
        self.assertEqual(self.event.seats_unconfirmed, 0)
        self.assertEqual(self.event.seats_reserved, 3)

    def test_event_session_is_ongoing(self):
        # Case 1: Session is ongoing
        session = self.env["event.session"].create(
            {
                "event_id": self.event.id,
                "date_begin": fields.Datetime.now() - timedelta(hours=1),
                "date_end": fields.Datetime.now() + timedelta(hours=1),
            }
        )
        ongoing = self.env["event.session"].search([("is_ongoing", "=", True)])
        not_ongoing = self.env["event.session"].search([("is_ongoing", "=", False)])
        self.assertTrue(session.is_ongoing)
        self.assertIn(session, ongoing)
        self.assertNotIn(session, not_ongoing)
        # Case 2: It isn't
        session.write(
            {
                "date_begin": fields.Datetime.now() + timedelta(days=1),
                "date_end": fields.Datetime.now() + timedelta(days=1, hours=1),
            }
        )
        ongoing = self.env["event.session"].search([("is_ongoing", "=", True)])
        not_ongoing = self.env["event.session"].search([("is_ongoing", "=", False)])
        self.assertFalse(session.is_ongoing)
        self.assertIn(session, not_ongoing)
        self.assertNotIn(session, ongoing)

    def test_event_session_is_finished(self):
        # Case 1: Session is finished
        session = self.env["event.session"].create(
            {
                "event_id": self.event.id,
                "date_begin": fields.Datetime.now() - timedelta(hours=2),
                "date_end": fields.Datetime.now() - timedelta(hours=1),
            }
        )
        finished = self.env["event.session"].search([("is_finished", "=", True)])
        not_finished = self.env["event.session"].search([("is_finished", "=", False)])
        self.assertTrue(session.is_finished)
        self.assertIn(session, finished)
        self.assertNotIn(session, not_finished)
        # Case 2: It isn't
        session.write(
            {
                "date_begin": fields.Datetime.now() + timedelta(days=1),
                "date_end": fields.Datetime.now() + timedelta(days=1, hours=1),
            }
        )
        finished = self.env["event.session"].search([("is_finished", "=", True)])
        not_finished = self.env["event.session"].search([("is_finished", "=", False)])
        self.assertFalse(session.is_finished)
        self.assertIn(session, not_finished)
        self.assertNotIn(session, finished)

    def test_event_session_registrations_open(self):
        with freeze_time("2017-05-26 20:30:00"):
            self.session.invalidate_recordset(["event_registrations_open"])
            self.assertTrue(self.session.event_registrations_open)
        with freeze_time("2017-05-30 20:00:00"):
            self.session.invalidate_recordset(["event_registrations_open"])
            self.assertFalse(self.session.event_registrations_open)

    def test_event_session_action_set_done(self):
        self.assertEqual(self.session.stage_id, self.stage_new)
        self.session.action_set_done()
        self.assertEqual(self.session.stage_id, self.stage_done)

    def test_event_session_gc(self):
        self.assertEqual(self.session.stage_id, self.stage_new)
        with freeze_time("2017-05-26 20:30:00"):
            self.env["event.session"]._gc_mark_events_done()
            self.assertEqual(self.session.stage_id, self.stage_new, "Not done yet")
        with freeze_time("2017-05-27 20:00:00"):
            self.env["event.session"]._gc_mark_events_done()
            self.assertEqual(self.session.stage_id, self.stage_done, "Done")

    def test_event_session_update_multi(self):
        """Test the session series update"""
        sessions = self.env["event.session"].create(
            [
                {
                    "event_id": self.event.id,
                    "date_begin": "2017-05-20 20:00:00",
                    "date_end": "2017-05-20 21:00:00",
                },
                {
                    "event_id": self.event.id,
                    "date_begin": "2017-05-21 20:00:00",
                    "date_end": "2017-05-21 21:00:00",
                },
                {
                    "event_id": self.event.id,
                    "date_begin": "2017-05-22 20:00:00",
                    "date_end": "2017-05-22 21:00:00",
                },
                {
                    "event_id": self.event.id,
                    "date_begin": "2017-05-23 20:00:00",
                    "date_end": "2017-05-23 21:00:00",
                },
            ]
        )
        sessions = sessions.with_context(active_test=False)
        session1, session2, session3, session4 = sessions
        # Case 1: Archive session 1
        session1.write({"active": False, "session_update": "this"})
        self.assertFalse(session1.active)
        self.assertTrue(session2.active)
        self.assertTrue(session3.active)
        self.assertTrue(session4.active)
        # Case 2: Archive all
        session2.write({"active": False, "session_update": "all"})
        self.assertFalse(session1.active)
        self.assertFalse(session2.active)
        self.assertFalse(session3.active)
        self.assertFalse(session4.active)
        # Case 3: Unarchive starting from session 3
        session3.write({"active": True, "session_update": "subsequent"})
        self.assertFalse(session1.active)
        self.assertFalse(session2.active)
        self.assertTrue(session3.active)
        self.assertTrue(session4.active)
