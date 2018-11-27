# Copyright 2017 Tecnativa - David Vidal
# Copyright 2017 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).

from odoo.tests import common
from odoo.exceptions import ValidationError


class EventSession(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(EventSession, cls).setUpClass()
        cls.event = cls.env['event.event'].create({
            'name': 'Test event',
            'date_begin': '2017-05-26 20:00:00',
            'date_end': '2017-05-30 22:00:00',
        })
        cls.session = cls.env['event.session'].create({
            'date_begin': '2017-05-26 20:00:00',
            'date_end': '2017-05-26 22:00:00',
            'event_id': cls.event.id,
        })
        cls.wizard = cls.env['wizard.event.session'].create({
            'event_id': cls.event.id,
            'mondays': True,
            'tuesdays': True,
            'wednesdays': True,
            'thursdays': True,
            'fridays': True,
            'sundays': True,
            'saturdays': False,
            'delete_existing_sessions': False,
            'session_hour_ids': [
                (0, 0, {'start_time': 20.0, 'end_time': 21.0}),
            ],
        })

    def test_session_name_get(self):
        self.assertEqual(
            self.session.name_get()[0][1], '[Test event] ' + self.session.name,
        )

    def test_check_beginning_date(self):
        self.session.date_begin = '2017-05-26 20:00:00'
        with self.assertRaises(ValidationError):
            self.session.date_begin = '2017-05-26 19:59:59'
        with self.assertRaises(ValidationError):
            self.session.date_end = '2017-05-30 22:00:01'

    def test_check_end_date(self):
        self.session.date_end = '2017-05-30 22:00:00'
        with self.assertRaises(ValidationError):
            self.session.date_end = '2017-05-30 22:00:01'
        with self.assertRaises(ValidationError):
            self.session.date_end = '2017-05-26 19:59:59'

    def test_check_zero_duration(self):
        with self.assertRaises(ValidationError), self.cr.savepoint():
            self.session.write({
                'date_begin': '2017-05-28 22:00:00',
                'date_end': '2017-05-28 22:00:00',
            })

    def test_compute_name(self):
        vals = {
            'date_begin': '2017-05-28 22:00:00',
            'date_end': '2017-05-28 23:00:00',
        }
        session = self.env['event.session'].new(vals)
        self.assertEqual(session.name, 'Sunday 28/05/17 22:00 - 23:00')
        session.date_begin = session.date_end = False
        self.assertEqual(session.name, '/')

    def test_wizard(self):
        """Test Session Generation Wizard"""
        self.event.date_end = '2017-06-11 23:59:59'
        self.event.date_begin = '2017-06-05 00:00:00'
        self.wizard.delete_existing_session = True
        self.wizard.action_generate_sessions()
        # delete previous sessions
        self.wizard.update({'delete_existing_sessions': True})
        self.wizard.action_generate_sessions()
        sessions = self.env['event.session'].search([
            ['event_id', '=', self.event.id]
        ])
        self.assertEqual(len(sessions), 6)
        with self.assertRaises(ValidationError), self.cr.savepoint():
            # session duration = 0
            self.wizard.update({'session_hour_ids': [
                (0, 0, {'start_time': 20.0, 'end_time': 20.0}),
            ],
            })
        with self.assertRaises(ValidationError), self.cr.savepoint():
            # hour invalidity
            self.wizard.update({'session_hour_ids': [
                (0, 0, {'start_time': 24.0, 'end_time': 24.1}),
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
            # schedules overlap
            self.wizard.update({'session_hour_ids': [
                (0, 0, {'start_time': 20.0, 'end_time': 21.0}),
                (0, 0, {'start_time': 19.5, 'end_time': 21.5}),
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
