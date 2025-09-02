# Copyright 2017-19 Tecnativa - David Vidal
# Copyright 2017 Tecnativa - Sergio Teruel
# Copyright 2025 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _compute_attendee_count(self):
        """Adapt registrations counter to multi quantity"""
        res = super()._compute_attendee_count()
        registration_model = self.env["event.registration"]
        domain = [("sale_order_id", "in", self.ids), ("state", "!=", "cancel")]
        domain_nomulti = domain + [("event_id.registration_multi_qty", "=", False)]
        orders_data_nomulti = registration_model._read_group(
            domain_nomulti, ["sale_order_id"], ["__count"]
        )
        domain_multi = domain + [("event_id.registration_multi_qty", "=", True)]
        orders_data_multi = registration_model._read_group(
            domain_multi, ["sale_order_id"], ["qty:sum"]
        )
        mapped_data_nomulti = {order.id: qty for order, qty in orders_data_nomulti}
        mapped_data_multi = {order.id: qty for order, qty in orders_data_multi}
        for sale_order in self:
            sale_order.attendee_count = mapped_data_nomulti.get(sale_order.id, 0)
            sale_order.attendee_count += mapped_data_multi.get(sale_order.id, 0)
        return res


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _init_registrations(self):
        """Update registrations on events with multi qty enabled"""
        if self.env.context.get("skip_event_sale_registration_multi_qty"):
            return super()._init_registrations()
        Registration = self.env["event.registration"].sudo()
        for so_line in self.filtered("event_id"):
            if not so_line.event_id.registration_multi_qty:
                super(SaleOrderLine, so_line)._init_registrations()
                continue
            product_uom_qty = so_line.product_uom_qty
            # Set temporarily the order line to one avoiding to create more
            # than one registration
            so_line.product_uom_qty = 1
            super(SaleOrderLine, so_line)._init_registrations()
            # Set the so line qty back and set the registration qty
            so_line.product_uom_qty = product_uom_qty
            registration = Registration.search(
                [("sale_order_line_id", "=", so_line.id)]
            )
            registration.qty = int(product_uom_qty)
