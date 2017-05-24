# -*- coding: utf-8 -*-
# Copyright 2017 Sergio Teruel <sergio.teruel@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import SavepointCase


class EventMailCase(SavepointCase):

    @classmethod
    def setUpClass(self):
        """Add some defaults to let the test run without an accounts chart."""
        super(EventMailCase, self).setUpClass()
        self.template1 = self.env['event.mail.template'].create({
            'name': 'Template test 01',
        })
        self.template2 = self.env['event.mail.template'].create({
            'name': 'Template test 01',
            'scheduler_template_ids': [(0, 0, {
                'interval_nbr': 15,
                'interval_unit': 'days',
                'interval_type': 'before_event',
                'template_id': self.env.ref('event.event_reminder').id})],
        })

    def test_event_template_config(self):
        # Store default template in event settings
        event_config = self.env['event.config.settings'].sudo().create({
            'event_mail_template_id': self.template1.id,
            'auto_confirmation': 1,
        })
        event_config.execute()
        config_template_id = self.env['ir.values'].get_default(
            'event.config.settings', 'event_mail_template_id')
        self.assertTrue(
            config_template_id,
            'Event Mail: Template store in default values')

        # Create an event
        vals = {
            'name': 'Event test',
            'date_begin': '2017-05-01',
            'date_end': '2017-06-01',
            'auto_confirm': False,
            'event_mail_template_id': self.template1.id,
        }
        event = self.env['event.event'].create(vals)
        event._onchange_event_mail_template_id()
        self.assertTrue(
            event.event_mail_ids,
            'Event Mail: mails scheduler created for this event')

        # Change template in event
        event.event_mail_template_id = self.template2
        event._onchange_event_mail_template_id()
        self.assertEqual(
            len(event.event_mail_ids), 1,
            'Event Mail: mails scheduler only one')

    def test_event_template_no_config(self):
        # Store default template in event settings
        event_config = self.env['event.config.settings'].sudo().create({
            'event_mail_template_id': False,
            'auto_confirmation': 1,
        })
        event_config.execute()
        config_template_id = self.env['ir.values'].get_default(
            'event.config.settings', 'event_mail_template_id')
        self.assertFalse(
            self.env['event.mail.template'].browse(
                config_template_id).exists(),
            'Event Mail: Template are not stored as default values')

        # Create an event
        vals = {
            'name': 'Event test',
            'date_begin': '2017-05-01',
            'date_end': '2017-06-01',
            'auto_confirm': False,
        }
        event = self.env['event.event'].create(vals)
        self.assertEqual(
            len(event.event_mail_ids), 0,
            'Event Mail: mails scheduler no created for this event')
