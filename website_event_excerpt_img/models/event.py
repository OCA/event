# Copyright 2016 Tecnativa - Jairo Llopis
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class EventEvent(models.Model):
    _inherit = "event.event"

    priority = fields.Selection(
        [("0", "Normal"), ("1", "Highlighted")],
        required=True,
        default="0",
        help="Importance of the event, as shown in website (if enabled).")
