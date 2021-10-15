# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)

from odoo import api, models


class Event(models.Model):
    _inherit = "event.event"

    @api.onchange("event_type_id")
    def _onchange_type(self):
        super()._onchange_type()

        if self.event_type_id.use_ticketing:
            for type_ticket in self.event_type_id.event_ticket_ids:
                ticket = self.event_ticket_ids.filtered(
                    lambda t: t.product_id == type_ticket.product_id
                    and t.price == type_ticket.price
                )
                if ticket:
                    ticket.show_in_website = type_ticket.show_in_website
