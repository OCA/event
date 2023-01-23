# Copyright 2016 Tecnativa - Sergio Teruel
# Copyright 2016 Tecnativa - Vicent Cubells
# Copyright 2018 Tecnativa - Pedro M. Baeza
# Copyright 2023 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime, timedelta

from odoo.tests import common, new_test_user


class TestEventEmailReminder(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        today = datetime.now()
        date_event_1 = today + timedelta(days=7)
        ctx = {
            "mail_create_nolog": True,
            "mail_create_nosubscribe": True,
            "mail_notrack": True,
            "no_reset_password": True,
        }
        cls.user_1 = new_test_user(
            cls.env,
            login="test01@test.com",
            context=ctx,
        )
        cls.user_2 = new_test_user(
            cls.env,
            login="test02@test.com",
            context=ctx,
        )
        stage = cls.env.ref("event.event_stage_booked")
        cls.event_model = cls.env["event.event"]
        cls.event_1 = cls.event_model.create(
            {
                "name": "Test 01",
                "date_begin": date_event_1,
                "date_end": date_event_1,
                "user_id": cls.user_1.id,
                "stage_id": stage.id,
            }
        )
        date_event_2 = today + timedelta(days=8)
        cls.event_2 = cls.event_model.create(
            {
                "name": "Test 01",
                "date_begin": date_event_2,
                "date_end": date_event_2,
                "user_id": cls.user_2.id,
                "stage_id": stage.id,
            }
        )
        cls.template_default = cls.env.ref(
            "event_email_reminder.event_email_reminder_template"
        )
        cls.template_default.lang = "en_EN"
        cls.template = cls.template_default.copy()
        cls.template.subject = "Hello test - copy"
        cls.mail = cls.env["mail.mail"]
        cls.stage_new = cls.env.ref("event.event_stage_new")

    def test_cron_run_default_values(self):
        # Default values events which start exactly in today + 7 days
        self.event_model.run_event_email_reminder()
        mails_to_send = self.mail.search(
            [
                ("subject", "=", "The events will be started soon"),
                ("email_to", "like", "test%@test.com"),
            ]
        )
        self.assertEqual(len(mails_to_send), 1)
        address = mails_to_send.mapped("email_to")
        self.assertEqual(self.user_1.email, address[0])

    def test_cron_run_custom_values(self):
        self.event_model.run_event_email_reminder(10, False, True)
        mails_to_send = self.mail.search(
            [
                ("subject", "=", "The events will be started soon"),
                ("email_to", "like", "test%@test.com"),
            ]
        )
        self.assertEqual(len(mails_to_send), 2)
        address = mails_to_send.mapped("email_to")
        self.assertEqual({self.user_1.email, self.user_2.email}, set(address))

    def test_cron_run_template(self):
        self.event_model.run_event_email_reminder(8, False, False, self.template.id)
        mails_to_send = self.mail.search(
            [
                ("subject", "=", "Hello test - copy"),
                ("email_to", "like", "test%@test.com"),
            ]
        )
        self.assertEqual(len(mails_to_send), 1)
        address = mails_to_send.mapped("email_to")
        self.assertEqual(self.user_2.email, address[0])

    def test_cron_run_draft_events(self):
        # Change the event to draft state
        self.event_2.stage_id = self.stage_new
        self.event_model.run_event_email_reminder(8, True, False)
        mails_to_send = self.mail.search(
            [
                ("subject", "=", "The events will be started soon"),
                ("email_to", "like", "test%@test.com"),
            ]
        )
        self.assertEqual(len(mails_to_send), 1)
        address = mails_to_send.mapped("email_to")
        self.assertEqual(self.user_2.email, address[0])

    def test_cron_run_partners(self):
        user = self.env["res.users"].create(
            {
                "login": "test_user_event_email_reminder",
                "name": "Test user",
                "email": "test_user_event_email_reminder@test.com",
            }
        )
        self.event_model.run_event_email_reminder(
            8,
            partner_ids=user.partner_id.ids,
        )
        mails_to_send = self.mail.search(
            [
                ("subject", "=", "The events will be started soon"),
                ("email_to", "like", "test%@test.com"),
            ]
        )
        self.assertEqual(len(mails_to_send), 1)
        address = mails_to_send.mapped("email_to")
        self.assertEqual(user.email, address[0])
