# Copyright 2019 Tecnativa S.L. - Alexandre Díaz
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models

from odoo.addons.mail.models.mail_render_mixin import format_datetime


class EventEvent(models.Model):
    _inherit = "event.event"

    # Located with predictable format
    date_begin_pred_located = fields.Char(
        compute="_compute_date_begin_pred_located",
        store=True,
    )
    date_end_pred_located = fields.Char(
        compute="_compute_date_end_pred_located",
        store=True,
    )

    @api.depends("date_begin", "date_tz")
    def _compute_date_begin_pred_located(self):
        for record in self:
            if record.date_begin:
                record.date_begin_pred_located = format_datetime(
                    self.with_context(use_babel=False).env,
                    record.date_begin,
                    tz=record.date_tz,
                    dt_format="YYYY-MM-dd HH:mm:SS",
                )
            else:
                record.date_begin_pred_located = False

    @api.depends("date_end", "date_tz")
    def _compute_date_end_pred_located(self):
        for record in self:
            if record.date_end:
                record.date_end_pred_located = format_datetime(
                    self.with_context(use_babel=False).env,
                    record.date_end,
                    tz=record.date_tz,
                    dt_format="YYYY-MM-dd HH:mm:SS",
                )
            else:
                record.date_end_pred_located = False
