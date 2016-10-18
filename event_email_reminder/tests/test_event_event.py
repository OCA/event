# -*- coding: utf-8 -*-
# © 2016 Sergio Teruel <sergio.teruel@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime, timedelta
import time

from openerp.tests.common import TransactionCase
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT


class TestEventEmailReminder(TransactionCase):

    def setUp(self):
        super(TestEventEmailReminder, self).setUp()
        today = time.strftime(DEFAULT_SERVER_DATE_FORMAT)
        date_event_1 = datetime.strptime(
            today, DEFAULT_SERVER_DATE_FORMAT) + timedelta(days=7)

        self.user_1 = self.env['res.users'].sudo().create({
            'name': 'user - test 01',
            'email': 'test01@test.com',
            'login': 'test01@test.com',
        })
        self.user_2 = self.env['res.users'].sudo().create({
            'name': 'user - test 02',
            'email': 'test02@test.com',
            'login': 'test02@test.com',
        })
        self.event_1 = self.env["event.event"].create({
            "name": "Test 01",
            "date_begin": date_event_1,
            "date_end": date_event_1,
            "user_id": self.user_1.id,
            "state": 'confirm',
        })
        date_event_2 = datetime.strptime(
            today, DEFAULT_SERVER_DATE_FORMAT) + timedelta(days=8)
        self.event_2 = self.env["event.event"].create({
            "name": "Test 01",
            "date_begin": date_event_2,
            "date_end": date_event_2,
            "user_id": self.user_2.id,
            "state": 'confirm',
        })
        self.template_default = self.env.ref(
            'event_email_reminder.event_email_reminder_template')
        self.template_default.lang = 'en_EN'
        self.template = self.template_default.copy()
        self.template.subject = 'Hello test - copy'
        self.mail = self.env['mail.mail']

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
