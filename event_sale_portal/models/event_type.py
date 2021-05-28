# Copyright 2021 Camptocamp SA - Iván Todorovich
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class EventType(models.Model):
    _inherit = "event.type"

    portal_badge_download = fields.Boolean(
        string="Portal Badge Download",
        help="If set, a download link will be provider for the customer to "
        "download badges directly from the Sale Order portal page.\n"
        "Optionally, you can configure a specific report to use.",
        default=True,
    )
