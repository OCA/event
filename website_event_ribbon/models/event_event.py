# Copyright 2026 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class EventEvent(models.Model):
    _inherit = "event.event"

    website_ribbon_id = fields.Many2one("event.event.ribbon")
