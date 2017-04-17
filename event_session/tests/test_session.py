# -*- coding: utf-8 -*-
# Copyright 2017 Tecnativa - David Vidal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0).

from odoo.tests import common
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta


class EventSession(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(EventSession, cls).setUpClass()
        cls.event = cls.env['event.event'].create({
            'name': 'Test event',
            'date_begin': datetime.today(),
            'date_end': datetime.today() + timedelta(days=7),
            'seats_availability': 'limited',
            'seats_max': '5',
            'seats_min': '1',
        })
        cls.session = cls.env['event.session'].create({
            'name': 'Test session',
            'date': datetime.today() + timedelta(days=1),
            'date_end': datetime.today() + timedelta(days=1),
            'event_id': cls.event.id,
            'start_time': 20.0,
            'end_time': 21.5,
            'seats_availability': cls.event.seats_availability,
            'seats_max': cls.event.seats_max,
            'seats_min': cls.event.seats_min,
        })
        cls.attendee = cls.env['event.registration'].create({
            'name': 'Test attendee',
            'event_id': cls.event.id,
            'session_id': cls.session.id,
        })
        cls.wizard = cls.env['wizard.event.session'].create({
            'event_id': cls.event.id,
            'mondays': True,
            'tuesdays': True,
            'wednesdays': True,
            'thursdays': True,
            'fridays': True,
            'sundays': True,
            'saturdays': True,
            'delete_existing_sessions': False,
            'session_hour_ids': [
                (0, 0, {'start_time': 20.0, 'end_time': 21.0}),
            ],
        })
        cls.template = cls.env['event.mail.template'].create({
            'name': 'Template test 01',
            'scheduler_template_ids': [(0, 0, {
                'interval_nbr': 15,
                'interval_unit': 'days',
                'interval_type': 'before_event',
                'template_id': cls.env.ref('event.event_reminder').id})],
        })

    def test_session_methods(self):
        """ Session methods """
        self.assertEqual(
            # name_get method
            self.session.name_get()[0][1],
            '[' + self.event.name + '] ' + self.session.name
        )
        with self.assertRaises(ValidationError), self.cr.savepoint():
            # out of range begining date
            self.session.update({
                'date': datetime.strptime(
                    self.event.date_begin, '%Y-%m-%d %H:%M:%S'
                ) - timedelta(days=1),
            })
        with self.assertRaises(ValidationError), self.cr.savepoint():
            # out of range begining date
            self.session.update({
                'date': datetime.strptime(
                    self.event.date_end, '%Y-%m-%d %H:%M:%S'
                ) + timedelta(days=1),
            })
        with self.assertRaises(ValidationError), self.cr.savepoint():
            # zero duration
            self.session.update({
                'start_time': 20.0,
                'end_time': 20.0,
            })
        # registrations button
        res = self.session.button_open_registration()
        attendees = self.env['event.registration'].search([
            ['session_id', '=', self.session.id]
        ])
        self.assertEqual(
            res['domain'],
            [('id', 'in', attendees.ids)]
        )
        # assign mail templates
        self.session._set_session_mail_ids(self.event.id)
        self.assertEqual(len(self.session.event_mail_ids), 3)
        self.session._set_session_mail_ids(self.template)
        self.assertEqual(len(self.session.event_mail_ids), 3)

    def test_session_seats(self):
        """ Session seat """
        self.assertEqual(
            self.event.seats_available,
            self.session.seats_available)
        self.assertEqual(
            self.event.seats_unconfirmed,
            self.session.seats_unconfirmed
        )
        self.assertEqual(
            self.event.seats_used,
            self.session.seats_used
        )
        with self.assertRaises(ValidationError), self.cr.savepoint():
            # check limit regs
            for i in range(int(self.session.seats_available)+1):
                self.env['event.registration'].create({
                    'name': 'Test Attendee',
                    'event_id': self.event.id,
                    'session_id': self.session.id,
                })

    def test_wizard(self):
        """Test Session Generation Wizard"""
        self.wizard.action_generate_sessions()
        # delete previous sessions
        self.wizard.update({'delete_existing_sessions': True})
        self.wizard.update({'event_mail_template_id': self.template})
        self.wizard.action_generate_sessions()
        sessions = self.env['event.session'].search([
            ['event_id', '=', self.event.id]
        ])
        for session in sessions:
            self.assertTrue(session.event_mail_ids)
            self.assertEqual(session.seats_max, self.event.seats_max)
            self.assertEqual(session.seats_availability,
                             self.event.seats_availability)
        with self.assertRaises(ValidationError), self.cr.savepoint():
            # session duration = 0
            self.wizard.update({'session_hour_ids': [
                (0, 0, {'start_time': 20.0, 'end_time': 20.0}),
            ],
            })
        with self.assertRaises(ValidationError), self.cr.savepoint():
            # schedules overlap
            self.wizard.update({'session_hour_ids': [
                (0, 0, {'start_time': 20.0, 'end_time': 21.0}),
                (0, 0, {'start_time': 20.5, 'end_time': 21.5}),
            ],
            })
        with self.assertRaises(ValidationError), self.cr.savepoint():
            # weekday not set
            self.wizard.update({
                'mondays': False,
                'tuesdays': False,
                'wednesdays': False,
                'thursdays': False,
                'fridays': False,
                'sundays': False,
                'saturdays': False,
            })
            self.wizard.action_generate_sessions()
