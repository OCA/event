# Copyright 2017 David Vidal<david.vidal@tecnativa.com>
# Copyright 2021 Moka Tourisme (https://www.mokatourisme.fr).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import SUPERUSER_ID, _, api, fields, models
from odoo.exceptions import ValidationError


class EventRegistration(models.Model):
    _inherit = "event.registration"

    use_sessions = fields.Boolean(
        related="event_id.use_sessions",
    )
    session_id = fields.Many2one(
        comodel_name="event.session",
        string="Session",
        ondelete="restrict",
    )
    # NOTE: Originally these fields are related to event_id.
    #       We make them computed to get the date from the session if needed.
    event_begin_date = fields.Datetime(
        related=None, compute="_compute_event_begin_date"
    )
    event_end_date = fields.Datetime(related=None, compute="_compute_event_end_date")

    @api.depends("event_id.date_begin", "session_id.date_begin", "use_sessions")
    def _compute_event_begin_date(self):
        for rec in self:
            if rec.use_sessions:
                rec.event_begin_date = rec.session_id.date_begin
            else:
                rec.event_begin_date = rec.event_id.date_begin

    @api.depends("event_id.date_end", "session_id.date_end", "use_sessions")
    def _compute_event_end_date(self):
        for rec in self:
            if rec.use_sessions:
                rec.event_end_date = rec.session_id.date_end
            else:
                rec.event_end_date = rec.event_id.date_end

    @api.constrains("session_id")
    def _check_seats_limit(self):
        # Needed to check if the registration can be created
        # when we try to save it.
        session_records = self.filtered("session_id")
        for rec in session_records:
            session = rec.session_id
            if (
                session.seats_limited
                and session.seats_max
                and session.seats_available < (1 if rec.state == "draft" else 0)
            ):
                raise ValidationError(_("No more seats available for this session."))

    def _update_mail_schedulers(self):
        # OVERRIDE to handle sessions' mail scheduler, not event ones.
        session_records = self.filtered("session_id")
        regular_records = self - session_records
        res = super(EventRegistration, regular_records)._update_mail_schedulers()
        # Similar to super, only we find the schedulers linked to the session
        open_registrations = session_records.filtered(lambda r: r.state == "open")
        if not open_registrations:
            return res
        onsubscribe_schedulers = (
            self.env["event.mail.session"]
            .sudo()
            .search(
                [
                    ("session_id", "in", open_registrations.session_id.ids),
                    ("interval_type", "=", "after_sub"),
                ]
            )
        )
        if not onsubscribe_schedulers:
            return res
        onsubscribe_schedulers.mail_done = False
        onsubscribe_schedulers.with_user(SUPERUSER_ID).execute()
        return res
