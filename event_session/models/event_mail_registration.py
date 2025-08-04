# Copyright 2021 Moka Tourisme (https://www.mokatourisme.fr).
# @author Iván Todorovich <ivan.todorovich@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models

from odoo.addons.event.models.event_mail import _INTERVALS


class EventMailRegistration(models.Model):
    _inherit = "event.mail.registration"

    session_scheduler_id = fields.Many2one(
        comodel_name="event.mail.session",
        string="Session Mail",
        ondelete="cascade",
    )

    @api.depends(
        "session_scheduler_id.interval_unit",
        "session_scheduler_id.interval_type",
    )
    def _compute_scheduled_date(self):
        # OVERRIDE to handle session mail registrations
        session_records = self.filtered("session_scheduler_id")
        regular_records = self - session_records
        for rec in session_records:
            if rec.registration_id:
                date_open = rec.registration_id.create_date.replace(microsecond=0)
                scheduler = rec.session_scheduler_id
                delta = _INTERVALS[scheduler.interval_unit](scheduler.interval_nbr)
                rec.scheduled_date = date_open + delta
            else:  # pragma: no cover
                rec.scheduled_date = False
        return super(EventMailRegistration, regular_records)._compute_scheduled_date()
