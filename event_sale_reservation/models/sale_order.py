# Copyright 2021 Tecnativa - Jairo Llopis
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    event_reservations_pending = fields.Integer(
        compute="_compute_event_reservations_pending",
        string="Pending event reservations",
        help=(
            "Indicates how many event reservations are still not linked to "
            "any registration."
        ),
    )

    @api.depends("order_line.product_uom_qty", "order_line.event_registration_count")
    def _compute_event_reservations_pending(self):
        """Know how many pending event reservations are linked to this SO."""
        for one in self:
            reservation_lines = one.order_line.filtered(
                lambda x: x.product_id.service_tracking == "event_reservation"
            )
            reserved = sum(reservation_lines.mapped("product_uom_qty"))
            registered = sum(reservation_lines.mapped("event_registration_count"))
            one.event_reservations_pending = reserved - registered
