# Copyright 2023 Camptocamp SA (https://www.camptocamp.com).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class EventTicket(models.Model):
    _inherit = "event.event.ticket"

    is_child_ticket = fields.Boolean(related="product_id.is_child_ticket")
