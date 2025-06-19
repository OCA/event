# Copyright 2023 Le Filament (https://le-filament.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import fields, models


class EventTicket(models.Model):
    _inherit = "event.event.ticket"
    _order = "sequence, event_id, price"

    sequence = fields.Integer("Ticket order", default=0)
