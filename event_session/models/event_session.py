# Copyright 2017 David Vidal<david.vidal@tecnativa.com>
# Copyright 2017 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from locale import setlocale, LC_ALL


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

    @api.multi
    @api.depends('date_begin', 'date_end')
    def _compute_name(self):
        setlocale(LC_ALL, locale=(self.env.lang, 'UTF-8'))
        for session in self:
            if not (session.date_begin and session.date_end):
                session.name = '/'
                continue
            date_begin = fields.Datetime.from_string(
                session.date_begin_located)
            date_end = fields.Datetime.from_string(session.date_end_located)
            dt_format = '%A %d/%m/%y %H:%M'
            name = date_begin.strftime(dt_format)
            if date_begin.date() == date_end.date():
                dt_format = '%H:%M'
            name += " - " + date_end.strftime(dt_format)
            session.name = name.capitalize()

    @api.multi
    def name_get(self):
        """Redefine the name_get method to show the event name with the event
        session.
        """
        res = []
        for item in self:
            res.append((item.id, "[%s] %s" % (item.event_id.name, item.name)))
        return res

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
            'date_begin': self.event_id.date_begin,
            'date_end': self.event_id.date_end,
        })

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
