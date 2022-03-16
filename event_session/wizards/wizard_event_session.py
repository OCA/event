# Copyright 2017 David Vidal<david.vidal@tecnativa.com>
# Copyright 2017 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import datetime, timedelta

from pytz import timezone, utc

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class WizardEventSession(models.TransientModel):
    _name = "wizard.event.session"
    _description = "Wizard for ease sessions creation"

    name = fields.Char(
        "Session info",
        required=True,
        help="It will be generated according to given parameters",
        default="/",
    )
    event_id = fields.Many2one(
        comodel_name="event.event",
        readonly=True,
        ondelete="cascade",
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
    mondays = fields.Boolean(help="Create sessions on Mondays")
    tuesdays = fields.Boolean(help="Create sessions on Tuesdays")
    wednesdays = fields.Boolean(help="Create sessions on Wednesdays")
    thursdays = fields.Boolean(help="Create sessions on Thursdays")
    fridays = fields.Boolean(help="Create sessions on Fridays")
    saturdays = fields.Boolean(help="Create sessions on Saturdays")
    sundays = fields.Boolean(help="Create sessions on Sundays")
    delete_existing_sessions = fields.Boolean(
        default=True,
        help="Check in order to delete every previous session for this event",
    )
    session_hour_ids = fields.One2many(
        comodel_name="wizard.event.session.hours",
        inverse_name="wizard_event_session_id",
        string="Hours",
    )
    event_mail_template_id = fields.Many2one(
        comodel_name="event.mail.template",
        string="Mail Schedule",
    )

    @api.constrains("session_hour_ids")
    def _avoid_overlapping_hours(self):
        for hour_a in self.session_hour_ids:
            for hour_b in self.session_hour_ids:
                if hour_a != hour_b:
                    if hour_a.start_time == hour_b.start_time:
                        raise ValidationError(_("There are overlapping hours!"))
                    elif hour_b.start_time < hour_a.start_time < hour_b.end_time:
                        raise ValidationError(_("There are overlapping hours!"))

    def weekdays(self):
        """Generate a tuple with the values for accessing days by index."""
        return (
            self.mondays,
            self.tuesdays,
            self.wednesdays,
            self.thursdays,
            self.fridays,
            self.saturdays,
            self.sundays,
        )

    def existing_sessions(self, date):
        """Return existing sessions that match some criteria."""
        # Todo: Improve match
        return self.env["event.session"].search(
            [
                ("event_id", "=", self.event_id.id),
                ("date_begin", "=", date),
                ("start_time", "=", self.start_time),
            ],
        )

    def _prepare_session_values(self, date_begin, date_end):
        vals = {
            "event_id": self.event_id.id,
            "date_begin": fields.Datetime.to_string(date_begin),
            "date_end": fields.Datetime.to_string(date_end),
        }
        mail_template = self.event_mail_template_id or self.env["ir.default"].get(
            "res.config.settings", "event_mail_template_id"
        )
        if mail_template:
            template_values = self.env["event.session"]._session_mails_from_template(
                self.event_id.id, mail_template
            )
            vals["event_mail_ids"] = template_values
        return vals

    def generate_sessions(self):
        self.ensure_one()
        session_obj = self.env["event.session"]
        event_start = utc.localize(self.event_date_begin)
        event_end = utc.localize(self.event_date_end)
        weekdays = self.weekdays()
        current = event_start
        current = current.replace(hour=event_end.hour, minute=event_end.minute)
        while current <= event_end:
            if not weekdays[current.weekday()]:
                current += timedelta(days=1)
                continue
            for hour in self.session_hour_ids:
                start_time = datetime.min + timedelta(hours=hour.start_time)
                end_time = datetime.min + timedelta(hours=hour.end_time)
                current_start = datetime.combine(
                    current.date(),
                    start_time.time(),
                )
                current_end = datetime.combine(current.date(), end_time.time())
                # Convert to UTC from user TZ
                local_tz = timezone(self.env.user.tz)
                current_start = local_tz.localize(current_start)
                current_start = current_start.astimezone(utc)
                current_end = local_tz.localize(current_end)
                current_end = current_end.astimezone(utc)
                if current_start < event_start or current_end > event_end:
                    continue
                # TODO: Check that no session exists with this data
                session_obj.create(
                    self._prepare_session_values(current_start, current_end)
                )
            current += timedelta(days=1)

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
    _description = "Hours in wich the sessions will run"

    wizard_event_session_id = fields.Many2one(comodel_name="wizard.event.session")
    start_time = fields.Float(required=True)
    end_time = fields.Float(required=True)

    # Todo: manage multiday sessions

    @api.constrains("start_time", "end_time")
    def _check_zero_duration(self):
        for hour in self:
            if hour.start_time == hour.end_time:
                raise ValidationError(_("There are sessions with no duration!"))

    @api.constrains("start_time", "end_time")
    def _check_hour_validity(self):
        for hour in self:
            if hour.start_time > 23.99 or hour.end_time > 23.99:
                raise ValidationError(_("You've entered invalid hours!"))
