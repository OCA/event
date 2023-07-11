# Copyright 2017 David Vidal<david.vidal@tecnativa.com>
# Copyright 2021 Moka Tourisme (https://www.mokatourisme.fr).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class EventMail(models.Model):
    _inherit = "event.mail"

    use_sessions = fields.Boolean(
        related="event_id.use_sessions",
    )
    session_scheduler_ids = fields.One2many(
        comodel_name="event.mail.session",
        inverse_name="scheduler_id",
        string="Session Mails",
    )

    @api.depends("event_id.use_sessions")
    def _compute_scheduled_date(self):
        # OVERRIDE to handle event session mail schedulers.
        # We set scheduled_date to False because it doesn't make sense for sessions,
        # as we use them only as "templates" to be copied/synced to the sessions as
        # `event.mail.session` records. Their scheduled_dates are then computed from
        # the dates of the related session.
        # By doing it, we get the additional benefit of having them automatically
        # ignored by the scheduled_date domain leaf of the core's mail scheduler cron.
        session_records = self.filtered("use_sessions")
        session_records.scheduled_date = False
        regular_records = self - session_records
        return super(EventMail, regular_records)._compute_scheduled_date()

    @api.model
    def schedule_communications(self, autocommit=False):
        # OVERRIDE to also process session mail schedulers
        res = super().schedule_communications(autocommit=autocommit)
        self.env["event.mail.session"].schedule_communications(autocommit=autocommit)
        return res

    def execute(self):  # pragma: no cover
        # OVERRIDE. Just in case, prevent execution of schedulers linked to event.event
        # that are using sessions. They manage that through event.mail.session.
        # This should never happen because they always have scheduled_date = False.
        session_records = self.filtered("use_sessions")
        regular_records = self - session_records
        if session_records:  # pragma: no cover
            _logger.error("Trying to execute event.mail linked to a session event.")
        return super(EventMail, regular_records).execute()

    def _prepare_session_mail_scheduler_vals(self, session):
        return {
            "scheduler_id": self.id,
            "session_id": session.id,
        }
