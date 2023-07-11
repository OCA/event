# Copyright 2017-19 Tecnativa - David Vidal
# Copyright 2017 Tecnativa - Pedro M. Baeza
# Copyright 2021 Moka Tourisme (https://www.mokatourisme.fr).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).

from datetime import timedelta

from freezegun import freeze_time

from odoo.tools import mute_logger

from .common import CommonEventSessionCase


class TestEventSession(CommonEventSessionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.mail_template_reminder = cls.env.ref("event_session.event_session_reminder")
        cls.mail_template_badge = cls.env.ref(
            "event_session.event_session_registration_mail_template_badge"
        )
        cls.event = cls.env["event.event"].create(
            {
                "name": "Test event",
                "use_sessions": True,
                "event_mail_ids": [
                    (0, 0, vals)
                    for vals in [
                        {
                            "interval_nbr": 15,
                            "interval_unit": "days",
                            "interval_type": "before_event",
                            "template_ref": f"mail.template,{cls.mail_template_reminder.id}",
                        },
                        {
                            "interval_nbr": 0,
                            "interval_unit": "hours",
                            "interval_type": "after_sub",
                            "template_ref": f"mail.template,{cls.mail_template_badge.id}",
                        },
                    ]
                ],
            }
        )
        cls.session = cls.env["event.session"].create(
            {
                "date_begin": "2017-05-26 20:00:00",
                "date_end": "2017-05-26 21:00:00",
                "event_id": cls.event.id,
            }
        )
        cls.registration = cls.env["event.registration"].create(
            {
                "name": "Test Attendee",
                "event_id": cls.event.id,
                "session_id": cls.session.id,
            }
        )
        cls.registration.action_confirm()

    @mute_logger("odoo.models.unlink")
    def test_event_mail_sync_from_event(self):
        self.assertEqual(len(self.session.event_mail_ids), 2)
        # Case 1: Remove from event, removes from sessions
        self.event.event_mail_ids[0].unlink()
        self.assertEqual(len(self.session.event_mail_ids), 1)
        # Case 2: Add a new template
        event_mail = self.env["event.mail"].create(
            {
                "event_id": self.event.id,
                "interval_nbr": 5,
                "interval_unit": "days",
                "interval_type": "before_event",
                "template_ref": f"mail.template,{self.mail_template_reminder.id}",
            }
        )
        session_mail = self.session.event_mail_ids.filtered(
            lambda r: r.scheduler_id == event_mail
        )
        self.assertTrue(session_mail)
        self.assertEqual(event_mail.interval_nbr, session_mail.interval_nbr)
        self.assertEqual(event_mail.interval_unit, session_mail.interval_unit)
        self.assertEqual(event_mail.interval_type, session_mail.interval_type)
        self.assertEqual(event_mail.template_ref, session_mail.template_ref)

    def test_event_mail_compute_scheduled_date(self):
        event_mail = self.event.event_mail_ids.filtered(
            lambda m: m.interval_type == "before_event"
        )
        session_mail = self.session.event_mail_ids.filtered(
            lambda m: m.scheduler_id == event_mail
        )
        # Case 1: 15 days before event
        event_mail.interval_nbr = 10
        expected = self.session.date_begin - timedelta(days=10)
        self.assertEqual(session_mail.scheduled_date, expected)
        self.assertFalse(event_mail.scheduled_date)
        # Case 2: 2 days after event
        event_mail.interval_nbr = 2
        event_mail.interval_type = "after_event"
        expected = self.session.date_end + timedelta(days=2)
        self.assertEqual(session_mail.scheduled_date, expected)
        self.assertFalse(event_mail.scheduled_date)
        # Case 3: after sub
        event_mail.interval_nbr = 0
        event_mail.interval_type = "after_sub"
        self.assertEqual(session_mail.scheduled_date, self.session.create_date)
        self.assertFalse(event_mail.scheduled_date)

    def test_event_mail_registration_compute_scheduled_date(self):
        session_mail = self.session.event_mail_ids.filtered(
            lambda m: m.interval_type == "after_sub"
        )
        self.env["event.registration"].create(
            {
                "name": "Test Attendee",
                "event_id": self.event.id,
                "session_id": self.session.id,
                "state": "open",
            }
        )
        mail_registration = session_mail._create_missing_mail_registrations(
            session_mail._get_new_event_registrations()
        )
        expected = mail_registration.registration_id.create_date
        self.assertEqual(mail_registration.scheduled_date, expected)

    @freeze_time("2017-05-16")
    def test_event_mail_session_scheduler(self):
        before_mail = self.session.event_mail_ids.filtered(
            lambda m: m.interval_type == "before_event"
        )
        self.assertFalse(before_mail.mail_done)
        self.env["event.mail"].schedule_communications()
        self.assertTrue(before_mail.mail_done)

    @freeze_time("2017-06-01")
    def test_event_mail_session_scheduler_before_event_ignore_old(self):
        """Test that we do not send emails if the mailing was scheduled before the event
        but the event is over"""
        before_mail = self.session.event_mail_ids.filtered(
            lambda m: m.interval_type == "before_event"
        )
        self.assertFalse(before_mail.mail_done)
        self.env["event.mail"].schedule_communications()
        self.assertFalse(before_mail.mail_done)
