# Copyright 2023 Le Filament (https://le-filament.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import fields, models


class EventTicket(models.Model):
    _inherit = "event.event.ticket"

    max_ticket_per_order = fields.Integer(string="Max. per order", default=0)
