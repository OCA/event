# Copyright 2023- Le Filament (https://le-filament.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class EventType(models.Model):
    _inherit = "event.type"

    event_privacy = fields.Selection(
        [
            ("public", "Public"),
            ("private_displayed", "Private displayed"),
            ("private_hidden", "Private hidden"),
        ],
        string="Event privacy",
        default="public",
        required=True,
    )
