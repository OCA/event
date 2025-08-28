# Copyright 2017 Tecnativa - David Vidal
# Copyright 2017 Tecnativa - Pedro M. Baeza
# Copyright 2021 Moka Tourisme (https://www.mokatourisme.fr).
# @author Iván Todorovich <ivan.todorovich@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import datetime, time, timedelta

import pytz
from dateutil import rrule
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import ValidationError

SELECT_FREQ_TO_RRULE = {
    "daily": rrule.DAILY,
    "weekly": rrule.WEEKLY,
    "monthly": rrule.MONTHLY,
    "yearly": rrule.YEARLY,
}

RRULE_WEEKDAYS = {
    "SUN": "SU",
    "MON": "MO",
    "TUE": "TU",
    "WED": "WE",
    "THU": "TH",
    "FRI": "FR",
    "SAT": "SA",
}


def freq_to_rrule(freq):
    return SELECT_FREQ_TO_RRULE[freq]


def float_time_to_hours_and_minutes(float_time):
    # Round to 2 decimals to avoid hours like 1:60
    # It'd be rounded to 2:00
    float_time = round(float_time, 2)
    hours = int(float_time)
    minutes = round((float_time - hours) * 60)
    return (hours, minutes)


def float_time_as_timedelta(float_time):
    hours, minutes = float_time_to_hours_and_minutes(float_time)
    return timedelta(hours=hours, minutes=minutes)


def float_time_as_time(float_time):
    hours, minutes = float_time_to_hours_and_minutes(float_time)
    return time(hour=hours, minute=minutes)


class WizardEventSession(models.TransientModel):
    _name = "wizard.event.session"
    _description = "Wizard for ease sessions creation"

    event_id = fields.Many2one(
        comodel_name="event.event",
        default=lambda self: self.env.context["id"],
        ondelete="cascade",
        required=True,
        readonly=True,
    )
    date_tz = fields.Selection(
        related="event_id.date_tz",
        help="Set it up in the event configuration"
        "Sessions will be generated up to this date",
    )
    duration = fields.Float(
        compute="_compute_duration",
        readonly=False,
        store=True,
        required=True,
        help="Duration of the sessions in hours",
    )
    timeslot_ids = fields.Many2many(
        comodel_name="event.session.timeslot",
        string="Time slots",
        required=True,
    )
    # rrule fields
    interval = fields.Integer(default=1, required=True)
    rrule_type = fields.Selection(
        [("weekly", "Weeks"), ("monthly", "Months")],
        string="Recurrence",
        default="weekly",
        required=True,
    )
    mon = fields.Boolean()
    tue = fields.Boolean()
    wed = fields.Boolean()
    thu = fields.Boolean()
    fri = fields.Boolean()
    sat = fields.Boolean()
    sun = fields.Boolean()
    month_by = fields.Selection(
        [("date", "Date of month"), ("day", "Day of month")],
        default="date",
    )
    day = fields.Integer(default=1)
    weekday = fields.Selection(
        [
            ("MON", "Monday"),
            ("TUE", "Tuesday"),
            ("WED", "Wednesday"),
            ("THU", "Thursday"),
            ("FRI", "Friday"),
            ("SAT", "Saturday"),
            ("SUN", "Sunday"),
        ],
    )
    byday = fields.Selection(
        [
            ("1", "First"),
            ("2", "Second"),
            ("3", "Third"),
            ("4", "Fourth"),
            ("-1", "Last"),
        ],
        string="By day",
    )
    start = fields.Date(
        compute="_compute_start",
        readonly=False,
        required=True,
        store=True,
    )
    until = fields.Date(required=True)

    @api.depends("event_id")
    def _compute_start(self):
        # Suggest to create sessions from the date of the last session
        # Usually the user wants to add new ones.
        for rec in self:
            rec.start = rec.event_id.date_end.date() + timedelta(days=1)

    @api.depends("event_id")
    def _compute_duration(self):
        # Suggest to create sessions with the same duration than the
        # last existing session
        for rec in self:
            if rec.event_id.session_ids:
                session = rec.event_id.session_ids[-1]
                delta = session.date_end - session.date_begin
                rec.duration = round(delta.total_seconds() / 3600, 2)

    @api.constrains("duration")
    def _check_duration(self):
        if any(rec.duration <= 0 for rec in self):
            raise ValidationError(self.env._("Duration is required."))

    @api.constrains("interval")
    def _check_interval(self):
        if any(rec.interval <= 0 for rec in self):
            raise ValidationError(self.env._("The interval cannot be negative."))

    def _get_lang_week_start(self):
        lang = self.env["res.lang"]._lang_get(self.env.user.lang)
        week_start = int(lang.week_start)
        # lang.week_start ranges from '1' to '7'
        # rrule expects an int from 0 to 6
        return rrule.weekday(week_start - 1)

    def _get_week_days(self):
        return tuple(
            rrule.weekday(weekday_index)
            for weekday_index, weekday in {
                rrule.MO.weekday: self.mon,
                rrule.TU.weekday: self.tue,
                rrule.WE.weekday: self.wed,
                rrule.TH.weekday: self.thu,
                rrule.FR.weekday: self.fri,
                rrule.SA.weekday: self.sat,
                rrule.SU.weekday: self.sun,
            }.items()
            if weekday
        )

    def _get_rrule(self, dtstart=None):
        """Builds the rrule from fields"""
        self.ensure_one()
        freq = self.rrule_type
        rrule_params = dict(
            dtstart=dtstart,
            until=datetime.combine(self.until, datetime.max.time()),
            interval=self.interval,
        )
        if freq == "monthly" and self.month_by == "date":
            rrule_params["bymonthday"] = self.day
        elif freq == "monthly" and self.month_by == "day":
            rrule_params["byweekday"] = getattr(rrule, RRULE_WEEKDAYS[self.weekday])(
                int(self.byday)
            )
        elif freq == "weekly":
            weekdays = self._get_week_days()
            if not weekdays:  # pragma: no cover
                raise ValidationError(
                    self.env._("You have to choose at least one day in the week")
                )
            rrule_params["byweekday"] = weekdays
            rrule_params["wkst"] = self._get_lang_week_start()
        return rrule.rrule(freq_to_rrule(freq), **rrule_params)

    def _get_start_of_period(self):
        self.ensure_one()
        dtstart = datetime.combine(self.start, datetime.min.time())
        if self.rrule_type == "monthly":
            return dtstart - relativedelta(day=1)
        return dtstart

    def _get_occurrences(self):
        self.ensure_one()
        dtstart = self._get_start_of_period()
        occurences = self._get_rrule(dtstart=dtstart)
        return list(occurences)

    def _get_ranges(self):
        """Generate ranges from the rrule

        :return: list of tuples (start_dt, end_dt, extra_vals)
        """
        self.ensure_one()
        res = []
        ocurrences = self._get_occurrences()
        duration = float_time_as_timedelta(self.duration)
        timezone = pytz.timezone(self.date_tz)
        timeslot_times = [float_time_as_time(t.time) for t in self.timeslot_ids]
        for dtstart in ocurrences:
            for tslot, ttime in zip(self.timeslot_ids, timeslot_times, strict=False):
                start = datetime.combine(dtstart, ttime)
                start_utc = (
                    timezone.localize(start, is_dst=False)
                    .astimezone(pytz.utc)
                    .replace(tzinfo=None)
                )
                extra_vals = tslot._prepare_session_extra_vals()
                res.append((start_utc, start_utc + duration, extra_vals))
        return res

    def _prepare_session_vals(self, date_begin, date_end):
        self.ensure_one()
        return {
            "event_id": self.event_id.id,
            "date_begin": date_begin,
            "date_end": date_end,
        }

    def _create_sessions(self):
        """Create sessions"""
        self.ensure_one()
        session_vals = []
        for date_begin, date_end, extra_vals in self._get_ranges():
            vals = self._prepare_session_vals(date_begin, date_end)
            vals.update(extra_vals)
            session_vals.append(vals)
        return self.env["event.session"].create(session_vals)

    def action_create_sessions(self):
        self.ensure_one()
        sessions = self._create_sessions()
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "event_session.act_event_session_event_form"
        )
        action["domain"] = [("id", "in", sessions.ids)]
        action["context"] = {
            "default_event_id": self.event_id.id,
            "search_default_event_id": self.event_id.id,
        }
        return action
