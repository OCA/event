# -*- coding: utf-8 -*-
# Copyright 2017 David Vidal<david.vidal@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class EventSession(models.Model):
    _name = 'event.session'
    _description = 'Event session'

    name = fields.Char(
        string='Session',
        required=True,
    )
    active = fields.Boolean(
        default=True,
    )
    event_id = fields.Many2one(
        comodel_name='event.event',
        string='Event',
    )
    seats_min = fields.Integer(
        string='Minimum seats',
    )
    seats_max = fields.Integer(
        string="Maximum seats",
    )
    seats_availability = fields.Selection(
        [('limited', 'Limited'), ('unlimited', 'Unlimited')],
        'Maximum Attendees', required=True, default='unlimited',
    )
    seats_reserved = fields.Integer(
        string='Reserved Seats', store=True, readonly=True,
        compute='_compute_seats',
    )
    seats_available = fields.Integer(
        oldname='register_avail', string='Available Seats',
        store=True, readonly=True, compute='_compute_seats')
    seats_unconfirmed = fields.Integer(
        oldname='register_prospect', string='Unconfirmed Seat Reservations',
        store=True, readonly=True, compute='_compute_seats')
    seats_used = fields.Integer(
        oldname='register_attended', string='Number of Participants',
        store=True, readonly=True, compute='_compute_seats')
    seats_expected = fields.Integer(
        string='Number of Expected Attendees',
        readonly=True, compute='_compute_seats')
    date = fields.Datetime(
        string="Session date",
        required=True,
    )
    date_end = fields.Datetime(
        string="Session date end",
        required=True,
    )
    start_time = fields.Float(
        required=True,
        help="Session start time",
    )
    end_time = fields.Float(
        required=True,
        help="Session end time",
    )
    registration_ids = fields.One2many(
        comodel_name='event.registration',
        inverse_name='session_id',
        string='Attendees',
        state={'done': [('readonly', True)]},
    )
    event_mail_ids = fields.One2many(
        comodel_name='event.mail',
        inverse_name='session_id',
        string='Mail Schedule',
        copy=True)

    @api.model
    def _set_session_mail_ids(self, event_id):
        return [(0, 0, {
            'event_id': event_id,
            'interval_unit': 'now',
            'interval_type': 'after_sub',
            'template_id': self.env.ref('event.event_subscription').id
        }), (0, 0, {
            'event_id': event_id,
            'interval_nbr': 2,
            'interval_unit': 'days',
            'interval_type': 'before_event',
            'template_id': self.env.ref('event.event_reminder').id
        }), (0, 0, {
            'event_id': event_id,
            'interval_nbr': 15,
            'interval_unit': 'days',
            'interval_type': 'before_event',
            'template_id': self.env.ref('event.event_reminder').id
        })]

    @api.multi
    def name_get(self):
        """Redefine the name_get method to show the event name with the event
        session.
        """
        res = []
        for item in self:
            res.append((item.id, "[%s] %s" % (item.event_id.name, item.name)))
        return res

    @api.model
    def create(self, vals):
        if 'event_mail_ids' not in vals:
            vals.update({
                'event_mail_ids': self._set_session_mail_ids(vals['event_id'])
            })
        return super(EventSession, self).create(vals)

    @api.multi
    @api.depends('seats_max', 'registration_ids.state')
    def _compute_seats(self):
        """Determine reserved, available, reserved but unconfirmed and used
        seats by session.
        """
        # initialize fields to 0
        for session in self:
            session.seats_unconfirmed = session.seats_reserved = \
                session.seats_used = session.seats_available = 0
        # aggregate registrations by event session and by state
        if self.ids:
            state_field = {
                'draft': 'seats_unconfirmed',
                'open': 'seats_reserved',
                'done': 'seats_used',
            }
            query = """
                SELECT session_id, state, count(session_id)
                FROM event_registration
                WHERE session_id IN %s AND state IN ('draft', 'open', 'done')
                GROUP BY session_id, state """
            self._cr.execute(query, (tuple(self.ids),))
            for session_id, state, num in self._cr.fetchall():
                session = self.browse(session_id)
                session[state_field[state]] += num
        # compute seats_available
        for session in self:
            if session.seats_max > 0:
                session.seats_available = session.seats_max - (
                    session.seats_reserved + session.seats_used)
            session.seats_expected = (
                session.seats_unconfirmed + session.seats_reserved +
                session.seats_used)

    @api.onchange('event_id')
    def onchage_event_selection(self):
        self.seats_min = self.event_id.seats_min
        self.seats_max = self.event_id.seats_max
        self.seats_availability = self.event_id.seats_availability
        self.date = self.event_id.date_begin_located

    @api.multi
    @api.constrains('seats_max', 'seats_available')
    def _check_seats_limit(self):
        for session in self:
            if (session.seats_availability == 'limited' and
                    session.seats_max and session.seats_available < 0):
                raise ValidationError(
                    _('No more available seats for this session.'))

    @api.multi
    @api.constrains('date')
    def _check_out_of_event_date_range(self):
        for session in self:
            if self.event_id.date_end_located < session.date or \
                    session.date < self.event_id.date_begin_located:
                raise ValidationError(
                    _("Session date is out of this event dates range")
                )

    @api.multi
    @api.constrains('start_time', 'end_time')
    def _check_zero_duration(self):
        for session in self:
            if session.end_time == session.start_time:
                raise ValidationError(
                    _("Ending and starting time can't be the same!")
                )

    @api.multi
    def button_open_registration(self):
        """Opens session registrations"""
        self.ensure_one()
        action = self.env.ref(
            'event.act_event_registration_from_event').read()[0]
        action['domain'] = [('id', 'in', self.registration_ids.ids)]
        action['context'] = {}
        return action
