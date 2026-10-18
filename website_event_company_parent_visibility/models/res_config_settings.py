# Copyright 2026 INVITU (<https://www.invitu.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    share_events_with_parents = fields.Boolean(
        related="company_id.share_events_with_parents",
        readonly=False,
    )
