# Copyright 2021 Tecnativa - Jairo Llopis
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class EventType(models.Model):
    _inherit = "event.type"

    reserved_sale_order_line_ids = fields.One2many(
        string="Reserved sale order lines",
        comodel_name="sale.order.line",
        inverse_name="event_reservation_type_id",
    )
    seats_reservation_total = fields.Integer(
        string="Reserved seats",
        compute="_compute_reservations_total",
        store=True,
        help="Seats reserved for events of this type.",
    )

    def _seats_reservation_domain(self):
        """Domain to select sale.order.line with pending reservations."""
        return [
            ("event_reservation_type_id", "in", self.ids),
            ("order_id.state", "in", ("sale", "done")),
            ("product_id.service_tracking", "=", "event_reservation"),
        ]

    @api.depends(
        "reserved_sale_order_line_ids.event_registration_count",
        "reserved_sale_order_line_ids.event_reservation_type_id",
        "reserved_sale_order_line_ids.order_id.state",
        "reserved_sale_order_line_ids.product_id.service_tracking",
        "reserved_sale_order_line_ids.product_uom_qty",
    )
    def _compute_reservations_total(self):
        """Get how many reserved seats exist."""
        results = self.env["sale.order.line"]._read_group(
            domain=self._seats_reservation_domain(),
            groupby=["event_reservation_type_id"],
            aggregates=["product_uom_qty:sum", "event_registration_count:sum"],
        )
        totals = {
            event_type.id: product_uom_qty - event_registration_count
            for event_type, product_uom_qty, event_registration_count in results
        }
        for one in self:
            one.seats_reservation_total = totals.get(one.id, 0)

    def action_open_sale_orders(self):
        """Display SO that include reservations."""
        sol = self.env["sale.order.line"].search(
            self._seats_reservation_domain(),
        )
        result = self.env["ir.actions.act_window"]._for_xml_id("sale.action_orders")
        result["domain"] = [("order_line", "in", sol.ids)]
        return result
