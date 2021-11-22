# Copyright 2017 David Vidal<david.vidal@tecnativa.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class EventEvent(models.Model):
    _inherit = "event.event"

    use_sessions = fields.Boolean(
        string="Event Sessions",
        help="Manage multiple sessions per event",
        compute="_compute_use_sessions",
        store=True,
        readonly=False,
    )
    session_ids = fields.One2many(
        comodel_name="event.session",
        inverse_name="event_id",
        string="Sessions",
    )
    session_count = fields.Integer(
        string="Sessions Count",
        compute="_compute_session_count",
    )
    date_begin = fields.Datetime(
        compute="_compute_date_begin",
        store=True,
        readonly=False,
    )
    date_end = fields.Datetime(
        compute="_compute_date_end",
        store=True,
        readonly=False,
    )

    @api.depends("event_type_id")
    def _compute_use_sessions(self):
        for rec in self:
            rec.use_sessions = rec.event_type_id.use_sessions

    @api.onchange("use_sessions")
    def _onchange_use_sessions(self):
        """
        Automatically fill date_begin and date_end if it's a use_session event.
        These fields are required but computed from sessions anyway.
        """
        if self.use_sessions and not self.date_begin:
            self.date_begin = fields.Datetime.now()
        if self.use_sessions and not self.date_end:
            self.date_end = fields.Datetime.now()

    @api.depends("session_ids")
    def _compute_session_count(self):
        groups = self.env["event.session"].read_group(
            domain=[("event_id", "in", self.ids)],
            fields=["event_id"],
            groupby=["event_id"],
        )
        result = {g["event_id"][0]: g["event_id_count"] for g in groups}
        for rec in self:
            rec.session_count = result.get(rec.id, 0)

    @api.depends("use_sessions", "session_ids.date_begin")
    def _compute_date_begin(self):
        session_records = self.filtered("use_sessions")
        regular_records = self - session_records
        # This is a core field. Play nice with other modules.
        # It is also why we compute date_begin and date_end separately.
        if hasattr(super(), "_compute_date_begin"):  # pragma: no cover
            super(EventEvent, regular_records)._compute_date_begin()
        if not session_records:  # pragma: no cover
            return
        groups = self.env["event.session"].read_group(
            domain=[("event_id", "in", session_records.ids)],
            fields=["event_id", "date_begin:min"],
            groupby=["event_id"],
        )
        data = {d["event_id"][0]: d["date_begin"] for d in groups}
        for rec in session_records:
            if data.get(rec.id):
                rec.date_begin = data.get(rec.id)

    @api.depends("use_sessions", "session_ids.date_end")
    def _compute_date_end(self):
        session_records = self.filtered("use_sessions")
        regular_records = self - session_records
        # This is a core field. Play nice with other modules.
        # It is also why we compute date_begin and date_end separately.
        if hasattr(super(), "_compute_date_end"):  # pragma: no cover
            super(EventEvent, regular_records)._compute_date_end()
        if not session_records:  # pragma: no cover
            return
        groups = self.env["event.session"].read_group(
            domain=[("event_id", "in", session_records.ids)],
            fields=["event_id", "date_end:max"],
            groupby=["event_id"],
        )
        data = {d["event_id"][0]: d["date_end"] for d in groups}
        for rec in session_records:
            if data.get(rec.id):
                rec.date_end = data.get(rec.id)

    def _check_seats_limit(self):  # pragma: no cover
        # OVERRIDE to ignore this constraint for event with sessions
        # Seat availability is checked on each session, not here.
        session_records = self.filtered("use_sessions")
        regular_records = self - session_records
        return super(EventEvent, regular_records)._check_seats_limit()

    @api.model_create_multi
    def create(self, vals_list):
        # OVERRIDE to automatically fill date_begin and date_end if they're
        # missing and it's a use_session event.
        # These fields are required but computed from sessions anyway.
        for vals in vals_list:
            if vals.get("use_sessions"):
                vals["date_begin"] = fields.Datetime.now()
                vals["date_end"] = fields.Datetime.now()
        return super().create(vals_list)

    def write(self, vals):
        # OVERRIDE to prevent the switch of use_sessions if the event has registrations
        # and to automatically subscribe the organizer to sessions, if it changes.
        if "use_sessions" in vals:
            if any(
                rec.use_sessions != vals["use_sessions"] and rec.registration_ids
                for rec in self
            ):
                raise ValidationError(
                    _("You can't enable/disable sessions on events with registrations.")
                )
            if not vals["use_sessions"]:
                self.with_context(active_test=False).session_ids.unlink()
        if vals.get("organizer_id"):
            self.session_ids.message_subscribe([vals["organizer_id"]])
        return super().write(vals)
