# Copyright 2017 Tecnativa - David Vidal
# Copyright 2017 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).
from dateutil.relativedelta import relativedelta

from odoo import _, fields
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
            'seats_availability': 'limited',
            'seats_max': '5',
            'seats_min': '1',
        })
        cls.session = cls.env['event.session'].create({
            'date_begin': '2017-05-26 20:00:00',
            'date_end': '2017-05-26 22:00:00',
            'event_id': cls.event.id,
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
            'thursdays': False,
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
        cls.scheduler = cls.env['event.mail'].create({
            'event_id': cls.event.id,
            'session_id': cls.session.id,
            'interval_type': 'after_sub',
            'template_id': cls.template.id,
        })
        cls.mail_registration = cls.env['event.mail.registration'].create({
            'scheduler_id': cls.scheduler.id,
            'registration_id': cls.attendee.id,
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

    def test_open_registrations(self):
        # registrations button
        res = self.session.button_open_registration()
        attendees = self.env['event.registration'].search([
            ['session_id', '=', self.session.id]
        ])
        self.assertEqual(res['domain'], [('id', 'in', attendees.ids)])

    def test_assign_mail_template(self):
        vals = ({
            'event_mail_ids':
                self.session._session_mails_from_template(self.event.id)
        })
        self.session.write(vals)
        self.assertEqual(len(self.session.event_mail_ids), 0)
        vals = ({
            'event_mail_ids':
                self.session._session_mails_from_template(self.event.id,
                                                          self.template)
        })
        self.session.write(vals)
        self.assertEqual(len(self.session.event_mail_ids), 1)

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
                    'state': 'open',
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
        self.wizard.update({'event_mail_template_id': self.template})
        with self.assertRaises(ValidationError) as error, self.cr.savepoint():
            self.wizard.action_generate_sessions()
            self.assertEqual(error, _("You are trying to delete one or more \
            sessions with active registrations"))
        self.attendee.session_id = False
        self.wizard.action_generate_sessions()
        sessions = self.env['event.session'].search([
            ['event_id', '=', self.event.id]
        ])
        self.assertEqual(len(sessions), 6)
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

    def test_event_mail_compute_scheduled_date(self):
        self.assertFalse(self.scheduler.scheduled_date)
        self.scheduler.event_id.update({'state': 'confirm'})
        date = fields.Datetime.from_string(
            self.scheduler.session_id.create_date
        ) + relativedelta(hours=+1)
        self.assertEqual(
            self.scheduler.scheduled_date,
            fields.Datetime.to_string(date)
        )
        self.scheduler.update({'interval_type': 'before_event'})
        date = fields.Datetime.from_string(
            self.scheduler.session_id.date_begin
        ) + relativedelta(hours=-1)
        self.assertEqual(
            self.scheduler.scheduled_date,
            fields.Datetime.to_string(date)
        )
        self.scheduler.update({'interval_type': 'after_event'})
        date = fields.Datetime.from_string(
            self.scheduler.session_id.date_end
        ) + relativedelta(hours=+1)
        self.assertEqual(
            self.scheduler.scheduled_date,
            fields.Datetime.to_string(date)
        )

    def test_event_mail_registration_compute_scheduled_date(self):
        self.scheduler.update({'interval_unit': 'days'})
        date = fields.Datetime.from_string(
            self.mail_registration.registration_id.date_open
        ) + relativedelta(days=+1)
        self.assertEqual(
            self.mail_registration.scheduled_date,
            fields.Datetime.to_string(date)
        )
