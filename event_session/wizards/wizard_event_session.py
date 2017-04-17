# -*- coding: utf-8 -*-
# Copyright 2017 David Vidal<david.vidal@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta
from time import strftime, strptime
from locale import setlocale, LC_ALL


class WizardEventSession(models.TransientModel):
    _name = "wizard.event.session"

    name = fields.Char(
        "Session info",
        required=True,
        help="It will be generated according to given parameters",
        default='/',
    )
    event_id = fields.Many2one(
        comodel_name="event.event",
        readonly=True,
        default=lambda self: self.env.context["active_id"],
        required=True,
    )
    event_date_begin = fields.Datetime(
        related="event_id.date_begin",
        readonly=True,
        help="Set it up in the event configuration"
             "Sessions will be generated from this date",
    )
    event_date_end = fields.Datetime(
        related="event_id.date_end",
        readonly=True,
        help="Set it up in the event configuration"
             "Sessions will be generated up to this date",
    )
    event_date_tz = fields.Selection(
        related="event_id.date_tz",
        readonly=True,
        help="Set it up in the event configuration"
             "Sessions will be generated up to this date",
    )
    mondays = fields.Boolean(
        help="Create sessions on Mondays",
    )
    tuesdays = fields.Boolean(
        help="Create sessions on Tuesdays",
    )
    wednesdays = fields.Boolean(
        help="Create sessions on Wednesdays",
    )
    thursdays = fields.Boolean(
        help="Create sessions on Thursdays",
    )
    fridays = fields.Boolean(
        help="Create sessions on Fridays",
    )
    saturdays = fields.Boolean(
        help="Create sessions on Saturdays",
    )
    sundays = fields.Boolean(
        help="Create sessions on Sundays",
    )
    delete_existing_sessions = fields.Boolean(
        help="Check in order to delete every previous session for this event"
    )
    session_hour_ids = fields.One2many(
        comodel_name='wizard.event.session.hours',
        inverse_name='wizard_event_session_id',
        string='Hours',
    )
    event_mail_template_id = fields.Many2one(
        comodel_name='event.mail.template',
        string='Mail Schedule Template',
    )

    @api.multi
    @api.constrains('session_hour_ids')
    def _avoid_overlapping_hours(self):
        for hour_a in self.session_hour_ids:
            for hour_b in self.session_hour_ids:
                if hour_a != hour_b:
                    if hour_a.start_time == hour_b.start_time:
                        raise ValidationError(
                            _("There are overlapping hours!")
                        )
                    elif hour_b.start_time < \
                            hour_a.start_time < hour_b.end_time:
                        raise ValidationError(
                            _("There are overlapping hours!")
                        )

    @api.multi
    def weekdays(self):
        return (self.mondays,
                self.tuesdays,
                self.wednesdays,
                self.thursdays,
                self.fridays,
                self.saturdays,
                self.sundays)

    @api.multi
    def datetime_fields(self):
        """Fields converted to Python's Datetime-based objects."""
        result = {
            "event_start": fields.Datetime.from_string(self.event_date_begin),
            "event_end": fields.Datetime.from_string(self.event_date_end),
            "day_delta": timedelta(days=1),
        }
        return result

    @api.multi
    def existing_sessions(self, date):
        """Return existing sessions that match some criteria."""
        # Todo: Improve match
        return self.env["event.session"].search(
            [("event_id", "=", self.event_id.id),
             ("date", "=", date),
             ("start_time", "=", self.start_time)],
        )

    def _get_session_mail_template(self, mail_template):
        vals = [(6, 0, [])]
        if isinstance(mail_template, int):
            mail_template = self.env['event.mail.template'].browse(
                mail_template)
        for scheduler in mail_template.scheduler_template_ids:
            vals.append((0, 0, {
                'event_id': self.event_id.id,
                'interval_nbr': scheduler.interval_nbr,
                'interval_unit': scheduler.interval_unit,
                'interval_type': scheduler.interval_type,
                'template_id': scheduler.template_id.id,
            }))
        return vals

    @api.multi
    def create_session(self, **values):
        """Create a new session record with the provided values."""
        setlocale(LC_ALL, locale=(self.env.lang, 'UTF-8'))
        data = {
            "name": "{} {} - {}".format(
                strftime('%A %d/%m/%y',
                         strptime(values["date"], "%Y-%m-%d %H:%M:%S")),
                "%02d:%02d" % divmod(values["start_time"]*60, 60),
                "%02d:%02d" % divmod(values["end_time"]*60, 60),
                ).capitalize(),
            "event_id": self.event_id.id,
            "date_end": '%s : %s' % (
                strftime('%Y-%m-%d', strptime(
                    values["date"], "%Y-%m-%d %H:%M:%S")),
                "%02d:%02d" % divmod(values["end_time"]*60, 60)),
            "start_time": values["start_time"],
            "end_time": values["end_time"],
            "seats_min": self.event_id.seats_min,
            "seats_max": self.event_id.seats_max,
            "seats_availability": self.event_id.seats_availability,
        }
        mail_template = (self.event_mail_template_id or
                         self.event_id._default_event_mail_template_id())
        if mail_template:
            data['event_mail_ids'] = self._get_session_mail_template(
                mail_template)
        else:
            data['event_mail_ids'] = []

        data.update(values)
        return self.env["event.session"].create(data)

    @api.multi
    def generate_sessions(self):
        self.ensure_one()
        counter = 0
        dt = self.datetime_fields()
        weekdays = self.weekdays()
        current = dt["event_start"]
        while current <= dt["event_end"]:
            for hour in self.session_hour_ids:
                tm = hour.time_fields()
                current_start = datetime.combine(
                    current.date(),
                    tm["start_time"].time()
                )
                if (current_start >= dt["event_start"] and
                        weekdays[current.weekday()]):
                    current_end = datetime.combine(
                        current.date(),
                        tm["end_time"].time()
                    )
                    if current_end <= dt["event_end"]:
                        current_start = \
                            fields.Datetime.to_string(current_start)
                        # TODO: Check that no session exists with this data
                        self.create_session(
                            date=current_start,
                            start_time=hour.start_time,
                            end_time=hour.end_time,
                            )
                        counter += 1
            # Next day
            current += dt["day_delta"]

    @api.multi
    def action_generate_sessions(self):
        """Here's where magic is triggered"""
        weekdays = self.weekdays()
        if not any(weekdays):
            raise ValidationError(_("You must select at least one weekday"))
        if self.delete_existing_sessions:
            self.event_id.session_ids.unlink()
        self.generate_sessions()


class WizardEventSessionHours(models.TransientModel):
    _name = "wizard.event.session.hours"

    wizard_event_session_id = fields.Many2one(
        comodel_name='wizard.event.session'
    )
    start_time = fields.Float(required=True)
    end_time = fields.Float(required=True)

    # Todo: manage multiday sessions

    @api.multi
    @api.constrains('start_time', 'end_time')
    def _check_zero_duration(self):
        for hour in self:
            if hour.start_time == hour.end_time:
                raise ValidationError(
                    _("There are sessions with no duration!")
                )

    @api.multi
    @api.constrains('start_time', 'end_time')
    def _check_hour_validity(self):
        for hour in self:
            if hour.start_time > 23.99 or hour.end_time > 23.99:
                raise ValidationError(
                    _("You've entered invalid hours!")
                )

    @api.multi
    def time_fields(self):
        """Format hours"""
        result = {
            "start_time": datetime.min + timedelta(hours=self.start_time),
            "end_time": datetime.min + timedelta(hours=self.end_time),
        }
        return result
