# Copyright 2023 Camptocamp SA (https://www.camptocamp.com).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _cart_update(
        self, product_id=None, line_id=None, add_qty=0, set_qty=0, **kwargs
    ):
        # Add a check to ensure the last parent ticket is not removed from cart
        # if there are remaining child tickets
        if add_qty or not line_id:
            return super()._cart_update(product_id, line_id, add_qty, set_qty, **kwargs)
        try:
            new_qty = float(set_qty)
        except ValueError:
            new_qty = -1
        line = self.env["sale.order.line"].browse(line_id)
        ticket = line.event_ticket_id

        if ticket and not ticket.is_child_ticket and new_qty == 0:
            # When removing a parent ticket, we need to check that no child ticket is
            # left alone, ie. there is no left child ticket, or there is at least one
            # other parent ticket.
            remaining_child_ticket_lines = self.order_line.filtered_domain(
                [
                    ("event_ticket_id.is_child_ticket", "=", True),
                    ("product_uom_qty", ">", 0),
                    ("event_id", "=", ticket.event_id.id),
                ]
            )
            remaining_parent_tickets_lines = self.order_line.filtered_domain(
                [
                    ("event_ticket_id.is_child_ticket", "=", False),
                    ("product_uom_qty", ">", 0),
                    ("id", "!=", line_id),
                    ("event_id", "=", ticket.event_id.id),
                ]
            )
            if remaining_child_ticket_lines and not remaining_parent_tickets_lines:
                values = {
                    "warning": self.env["website"]
                    .get_current_website()
                    .website_event_sale_constraint_message,
                    "line_id": line_id,
                    "quantity": line.product_uom_qty,  # Former quantity
                }
                return values

        return super()._cart_update(product_id, line_id, add_qty, set_qty, **kwargs)
