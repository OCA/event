# Copyright 2017 David Vidal<david.vidal@tecnativa.com>
# Copyright 2017 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
import babel
from babel.dates import format_datetime, format_time


def get_locale(env):
    """
    Get the locale from the environment as done in ir.qweb.field

    https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/models/ir_qweb_fields.py#L235
    """
    lang = env['ir.qweb.field'].user_lang()
    locale = babel.Locale.parse(lang.code)
    return locale


def localized_format(value, formats, locale):
    """
    Return a string separated by spaces of the formatted
    value based on the locale passed as argument.
    """
    values = [
        dt_format(value, locale)
        for dt_format in formats
    ]
    return " ".join(values)


def time_format(dt_format):
    """
    Returns a callable that will format a datetime with a locale
    using the format_time method of babel.
    """
    def wrap(value, locale):
        return format_time(value, dt_format, locale=locale)
    return wrap


def datetime_format(dt_format):
    """
    Returns a callable that will format a datetime with a locale
    using the format_datetime method of babel.
    """
    def wrap(value, locale):
        return format_datetime(value, dt_format, locale=locale)
    return wrap


class EventSession(models.Model):
    _name = 'event.session'
    _description = 'Event session'

    name = fields.Char(
        string='Session', required=True, compute="_compute_name", store=True,
        default='/',
    )
    active = fields.Boolean(
        default=True,
    )
    company_id = fields.Many2one(
        comodel_name='res.company',
        related='event_id.company_id',
        store=True,
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
        readonly=True, compute='_compute_seats',
        store=True)
    seats_available_expected = fields.Integer(
        string='Available Expected Seats',
        readonly=True, compute='_compute_seats',
        store=True)
    seats_available_pc = fields.Float(
        string='Full %',
        readonly=True,
        compute='_compute_seats',
    )
    date_tz = fields.Selection(
        string='Timezone', related="event_id.date_tz",
    )
    date_begin = fields.Datetime(
        string="Session start date",
        required=True,
        default=lambda self: self.event_id.date_begin,
    )
    date_end = fields.Datetime(
        string="Session date end",
        required=True,
        default=lambda self: self.event_id.date_end,
    )
    date_begin_located = fields.Datetime(
        string='Start Date Located', compute='_compute_date_begin_located',
    )
    date_end_located = fields.Datetime(
        string='End Date Located', compute='_compute_date_end_located',
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
        copy=True
    )

    @api.multi
    @api.depends('date_begin', 'date_end')
    def _compute_name(self):
        locale = get_locale(self.env)
        for session in self:
            if not (session.date_begin and session.date_end):
                session.name = '/'
                continue
            date_begin = fields.Datetime.from_string(
                session.date_begin_located
            )
            date_end = fields.Datetime.from_string(
                session.date_end_located
            )

            dt_formats = [
                datetime_format("EEEE"),
                datetime_format("short")
            ]

            name = localized_format(date_begin, dt_formats, locale)

            if date_begin.date() == date_end.date():
                dt_formats = [
                    time_format("short")
                ]

            name = "%s - %s" % (
                name,
                localized_format(date_end, dt_formats, locale)
            )
            session.name = name

    def _session_mails_from_template(self, event_id, mail_template=None):
        vals = [(6, 0, [])]
        if not mail_template:
            mail_template = self.env['ir.default'].get(
                'res.config.settings', 'event_mail_template_id')
            if not mail_template:
                # Not template scheduler defined in event settings
                return vals
        if isinstance(mail_template, int):
            mail_template = self.env['event.mail.template'].browse(
                mail_template)
        for scheduler in mail_template.scheduler_template_ids:
            vals.append((0, 0, {
                'event_id': event_id,
                'interval_nbr': scheduler.interval_nbr,
                'interval_unit': scheduler.interval_unit,
                'interval_type': scheduler.interval_type,
                'template_id': scheduler.template_id.id,
            }))
        return vals

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
        # Config availabilities based on event
        if vals.get('event_id', False):
            event = self.env['event.event'].browse(vals.get('event_id'))
            vals['seats_availability'] = event.seats_availability
            vals['seats_max'] = event.seats_max
        if not vals.get('event_mail_ids', False):
            vals.update({
                'event_mail_ids':
                    self._session_mails_from_template(vals['event_id'])
            })
        return super(EventSession, self).create(vals)

    @api.multi
    def unlink(self):
        for this in self:
            if this.registration_ids:
                raise ValidationError(_("You are trying to delete one or more \
                sessions with active registrations"))
        return super(EventSession, self).unlink()

    @api.multi
    @api.depends('seats_max', 'registration_ids.state')
    def _compute_seats(self):
        """Determine reserved, available, reserved but unconfirmed and used
        seats by session.
        """
        # aggregate registrations by event session and by state
        if len(self.ids) > 0:
            state_field = {
                'draft': 'seats_unconfirmed',
                'open': 'seats_reserved',
                'done': 'seats_used',
            }
            result = self.env['event.registration'].read_group([
                ('session_id', 'in', self.ids),
                ('state', 'in', ['draft', 'open', 'done'])
            ], ['state', 'session_id'], ['session_id', 'state'], lazy=False)
            for res in result:
                session = self.browse(res['session_id'][0])
                session[state_field[res['state']]] += res['__count']
        # compute seats_available
        for session in self:
            if session.seats_max > 0:
                session.seats_available = session.seats_max - (
                    session.seats_reserved + session.seats_used)
            session.seats_expected = (
                session.seats_unconfirmed + session.seats_reserved +
                session.seats_used)
            session.seats_available_expected = (
                session.seats_max - session.seats_expected)
            if session.seats_max > 0:
                session.seats_available_pc = (
                    session.seats_expected * 100 / float(session.seats_max))

    @api.multi
    @api.depends('date_tz', 'date_begin')
    def _compute_date_begin_located(self):
        for session in self.filtered('date_begin'):
            self_in_tz = session.with_context(
                tz=(session.date_tz or 'UTC')
            )
            date_begin = fields.Datetime.from_string(session.date_begin)
            session.date_begin_located = fields.Datetime.to_string(
                fields.Datetime.context_timestamp(self_in_tz, date_begin),
            )

    @api.multi
    @api.depends('date_tz', 'date_end')
    def _compute_date_end_located(self):
        for session in self.filtered('date_end'):
            self_in_tz = session.with_context(
                tz=(session.date_tz or 'UTC')
            )
            date_end = fields.Datetime.from_string(session.date_end)
            session.date_end_located = fields.Datetime.to_string(
                fields.Datetime.context_timestamp(self_in_tz, date_end),
            )

    @api.onchange('event_id')
    def onchange_event_id(self):
        self.update({
            'seats_min': self.event_id.seats_min,
            'seats_max': self.event_id.seats_max,
            'seats_availability': self.event_id.seats_availability,
            'date_begin': self.event_id.date_begin,
            'date_end': self.event_id.date_end,
        })

    @api.multi
    @api.constrains('seats_max', 'seats_available')
    def _check_seats_limit(self):
        for session in self:
            if (session.seats_availability == 'limited' and
                    session.seats_max and session.seats_available < 0):
                raise ValidationError(
                    _('No more available seats for this session.'))

    @api.multi
    @api.constrains('date_begin', 'date_end')
    def _check_dates(self):
        for session in self:
            if (self.event_id.date_end < session.date_begin or
                    session.date_begin < self.event_id.date_begin or
                    self.event_id.date_begin > session.date_end or
                    session.date_end > self.event_id.date_end):
                raise ValidationError(
                    _("Session date is out of this event dates range")
                )

    @api.multi
    @api.constrains('date_begin', 'date_end')
    def _check_zero_duration(self):
        for session in self:
            if session.date_begin == session.date_end:
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
        action['context'] = {
            'default_event_id': self.event_id.id,
            'default_session_id': self.id,
        }
        return action
