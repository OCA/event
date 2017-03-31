# -*- coding: utf-8 -*-
# © 2016 Sergio Teruel <sergio.teruel@tecnativa.com>
# © 2016 Vicent Cubells <vicent.cubells@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import timedelta
from openerp.tests.common import SavepointCase
from openerp import fields


class TestEventEmailReminder(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestEventEmailReminder, cls).setUpClass()
        today = fields.Date.today()
        date_event_1 = fields.Date.from_string(today) + timedelta(days=7)
        cls.user_1 = cls.env['res.users'].sudo().create({
            'name': 'user - test 01',
            'email': 'test01@test.com',
            'login': 'test01@test.com',
        })
        cls.user_2 = cls.env['res.users'].sudo().create({
            'name': 'user - test 02',
            'email': 'test02@test.com',
            'login': 'test02@test.com',
        })
        cls.event_1 = cls.env["event.event"].create({
            "name": "Test 01",
            "date_begin": date_event_1,
            "date_end": date_event_1,
            "user_id": cls.user_1.id,
            "state": 'confirm',
        })
        date_event_2 = fields.Date.from_string(today) + timedelta(days=8)
        cls.event_2 = cls.env["event.event"].create({
            "name": "Test 01",
            "date_begin": date_event_2,
            "date_end": date_event_2,
            "user_id": cls.user_2.id,
            "state": 'confirm',
        })
        cls.template_default = cls.env.ref(
            'event_email_reminder.event_email_reminder_template')
        cls.template_default.lang = 'en_EN'
        cls.template = cls.template_default.copy()
        cls.template.subject = 'Hello test - copy'
        cls.mail = cls.env['mail.mail']

    def test_cron_run_default_values(self):
        # Default values events which start exactly in today + 7 days
        self.env['event.event'].run_event_email_reminder()
        mails_to_send = self.mail.search([
            ('subject', '=', 'The events will be started soon'),
            ('email_to', 'like', 'test%@test.com'),
        ])
        self.assertEqual(len(mails_to_send), 1)
        address = mails_to_send.mapped('email_to')
        self.assertEqual(self.user_1.email, address[0])

    def test_cron_run_custom_values(self):
        self.env['event.event'].run_event_email_reminder(10, False, True)
        mails_to_send = self.mail.search([
            ('subject', '=', 'The events will be started soon'),
            ('email_to', 'like', 'test%@test.com'),
        ])
        self.assertEqual(len(mails_to_send), 2)
        address = mails_to_send.mapped('email_to')
        self.assertEqual(
            set([self.user_1.email, self.user_2.email]), set(address))

    def test_cron_run_template(self):
        self.env['event.event'].run_event_email_reminder(
            8, False, False, self.template.id)
        mails_to_send = self.mail.search([
            ('subject', '=', 'Hello test - copy'),
            ('email_to', 'like', 'test%@test.com'),
        ])
        self.assertEqual(len(mails_to_send), 1)
        address = mails_to_send.mapped('email_to')
        self.assertEqual(self.user_2.email, address[0])

    def test_cron_run_draft_events(self):
        # Change the event to draft state
        self.event_2.state = 'draft'
        self.env['event.event'].run_event_email_reminder(8, True, False)
        mails_to_send = self.mail.search([
            ('subject', '=', 'The events will be started soon'),
            ('email_to', 'like', 'test%@test.com'),
        ])
        self.assertEqual(len(mails_to_send), 1)
        address = mails_to_send.mapped('email_to')
        self.assertEqual(self.user_2.email, address[0])
