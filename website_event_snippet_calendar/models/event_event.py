# Copyright 2019 Tecnativa S.L. - Alexandre Díaz
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.tools.misc import format_datetime


class EventEvent(models.Model):
    _inherit = "event.event"

    # Located with predictable format
    date_begin_pred_located = fields.Char(
        compute="_compute_date_begin_pred_located",
        store=True,
    )

    @api.depends("date_begin", "date_tz")
    def _compute_date_begin_pred_located(self):
        for record in self:
            record.date_begin_pred_located = format_datetime(
                self.with_context(use_babel=False).env,
                record.date_begin,
                tz=record.date_tz,
                dt_format="YYYY-MM-dd HH:mm:SS",
            )
