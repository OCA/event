# Copyright 2021 Camptocamp SA - Iván Todorovich
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class EventEvent(models.Model):
    _inherit = "event.event"

    portal_badge_download = fields.Boolean(
        string="Portal Badge Download",
        help="If set, a download link will be provider for the customer to "
        "download badges directly from the Sale Order portal page.\n"
        "Optionally, you can configure a specific report to use.",
        default=True,
    )

    @api.onchange("event_type_id")
    def _onchange_type(self):
        res = super()._onchange_type()
        if self.event_type_id:
            self.portal_badge_download = self.event_type_id.portal_badge_download
        return res
