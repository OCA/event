# Copyright 2024 Tecnativa - Pilar Vargas
from odoo import fields, models


class EventEvent(models.Model):
    _inherit = "event.event"

    registration_membership_only = fields.Boolean(
        help="Allow registration only to members"
    )
