# Copyright 2017-22 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models

from odoo.addons.event.models.event_mail import _INTERVALS


class EventMailScheduler(models.Model):
    _inherit = "event.mail"

    event_id = fields.Many2one(required=False)
    session_id = fields.Many2one(
        comodel_name="event.session",
        string="Session",
        ondelete="cascade",
    )
    event_mail_template_id = fields.Many2one(
        comodel_name="event.mail.template",
        string="Event Mail Template",
        ondelete="cascade",
    )

    @api.depends()
    def _compute_done(self):
        super()._compute_done()
        for event_mail in self:
            if event_mail.session_id and event_mail.interval_type not in [
                "before_event",
                "after_event",
            ]:
                event_mail.done = (
                    True
                    if event_mail.event_id.sessions_count > 0
                    and not event_mail.session_id
                    else len(event_mail.mail_registration_ids)
                    == len(event_mail.session_id.registration_ids)
                    and all(line.mail_sent for line in event_mail.mail_registration_ids)
                )

    @api.depends("session_id.date_begin", "session_id.date_end")
    def _compute_scheduled_date(self):
        super()._compute_scheduled_date()
        for event_mail in self:
            if not event_mail.session_id:
                continue
            if event_mail.interval_type == "after_sub":
                date, sign = event_mail.session_id.create_date, 1
            elif event_mail.interval_type == "before_event":
                date, sign = event_mail.session_id.date_begin, -1
            else:
                date, sign = event_mail.session_id.date_end, 1
            event_mail.scheduled_date = date + _INTERVALS[event_mail.interval_unit](
                sign * event_mail.interval_nbr
            )


class EventMailRegistration(models.Model):
    _inherit = "event.mail.registration"

    @api.depends()
    def _compute_scheduled_date(self):
        super()._compute_scheduled_date()
        for event_mail_reg in self:
            if (
                event_mail_reg.registration_id
                and event_mail_reg.registration_id.session_id
            ):
                date_open = event_mail_reg.registration_id.date_open
                date_open_datetime = date_open and date_open or fields.datetime.now()
                event_mail_reg.scheduled_date = date_open_datetime + _INTERVALS[
                    event_mail_reg.scheduler_id.interval_unit
                ](event_mail_reg.scheduler_id.interval_nbr)
