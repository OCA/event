# Copyright 2023 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class EventType(models.Model):
    _inherit = "event.type"

    default_registration_min = fields.Integer(
        "Minimum Registrations",
        compute="_compute_default_registration_min",
        readonly=False,
        store=True,
        help="It will select this default minimum value when you choose this event",
    )

    @api.depends("has_seats_limitation")
    def _compute_default_registration_min(self):
        self.filtered(lambda x: not x.has_seats_limitation).default_registration_min = 0
