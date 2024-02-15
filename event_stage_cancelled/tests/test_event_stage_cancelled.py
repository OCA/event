# Copyright 2024 Tecnativa S.L. - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.tests import TransactionCase


class TestEventCancelCase(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.event = cls.env["event.event"].create(
            {
                "date_begin": "2024-05-06 09:00:00",
                "date_end": "2024-05-08 18:00:00",
                "name": "OCA DAYS",
            }
        )
        # Let's prevent default schedulers that could distort our test case
        cls.event.event_mail_ids.unlink()
        cls.mail_template = cls.env["mail.template"].create(
            {
                "name": "Test event cancelled",
                "model_id": cls.env.ref("event.model_event_registration").id,
                # Just a test, the event will go perfectly. Join it!
                "subject": "The event is cancelled!",
                "body_html": "<p>We're sorry to announce that...</p>",
            }
        )
        cls.event_mail = cls.env["event.mail"].create(
            [
                {
                    "event_id": cls.event.id,
                    "notification_type": "mail",
                    "interval_unit": "now",
                    "interval_type": "after_cancel",
                    "template_ref": f"mail.template, {cls.mail_template.id}",
                }
            ]
        )
        cls.attendees = cls.env["event.registration"].create(
            [
                {
                    "event_id": cls.event.id,
                    "name": f"Test attendee {reg}",
                    "email": f"test_attendee_{reg}@test.com",
                }
                for reg in range(5)
            ]
        )
        (
            cls.attendee_1,
            cls.attendee_2,
            cls.attendee_3,
            cls.attendee_4,
            cls.attendee_5,
        ) = cls.attendees
        # Let's add some variations
        (cls.attendee_1 + cls.attendee_2).state = "draft"
        (cls.attendee_3 + cls.attendee_4).state = "open"
        cls.attendee_5.state = "cancel"

    def test_event_cancellation(self):
        """Test the processes triggered by the event cancellation"""
        # Force the scheduler to see no effect (normally is handled by the cron)
        self.event_mail.execute()
        self.assertFalse(bool(self.event_mail.mail_registration_ids))
        self.assertFalse(self.event_mail.scheduled_date)
        self.assertEqual(self.event_mail.mail_state, "running")
        # Inject bypass_reason for test compatibility with event_registration_cancel_reason
        self.event.button_cancel()
        self.assertTrue(
            all([a.state == "cancel" for a in self.attendees]),
            f"Not all the attendees are cancelled: "
            f"{' / '.join([str((a.name, a.state)) for a in self.attendees])}",
        )
        # One attendee was already cancelled.
        self.assertEqual(len(self.attendees.filtered("cancelled_from_event")), 4)
        self.assertEqual(self.event_mail.mail_state, "scheduled")
        # Force the scheduler. Normally is handled by the cron
        self.event_mail.execute()
        # Only the attendees that we just cancelled are going to be notified
        self.assertEqual(
            (self.attendee_1 + self.attendee_2 + self.attendee_3 + self.attendee_4),
            self.event_mail.mail_registration_ids.registration_id,
        )
        self.assertEqual(self.event_mail.mail_state, "sent")
        self.assertTrue(all(self.event_mail.mail_registration_ids.mapped("mail_sent")))
