# Copyright 2019 Tecnativa S.L. - Alexandre Díaz
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.addons.mail.models.mail_template import format_tz
from odoo import fields, models, api, tools


class EventEvent(models.Model):
    _inherit = 'event.event'

    # Located with predictable format
    date_begin_pred_located = fields.Char(
        compute='_compute_date_begin_pred_located',
        store=True,
    )

    @api.multi
    @api.depends('date_begin', 'date_tz')
    def _compute_date_begin_pred_located(self):
        for record in self:
            record.date_begin_pred_located = format_tz(
                self.with_context(use_babel=False).env,
                record.date_begin,
                tz=record.date_tz,
                format=tools.DEFAULT_SERVER_DATETIME_FORMAT)
