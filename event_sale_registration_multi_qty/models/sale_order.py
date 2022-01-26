# Copyright 2017-19 Tecnativa - David Vidal
# Copyright 2017 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _update_registrations(
        self, confirm=True, cancel_to_draft=False, registration_data=None
    ):
        """Update registrations on events with multi qty enabled"""
        if self.env.context.get("skip_event_sale_registration_multi_qty"):
            return super()._update_registrations(
                confirm=confirm,
                cancel_to_draft=cancel_to_draft,
                registration_data=registration_data,
            )
        Registration = self.env["event.registration"]
        for so_line in self.filtered("event_id"):
            if not so_line.event_id.registration_multi_qty:
                super(SaleOrderLine, so_line)._update_registrations(
                    confirm=confirm,
                    cancel_to_draft=cancel_to_draft,
                    registration_data=registration_data,
                )
                continue
            product_uom_qty = so_line.product_uom_qty
            # Set temporarily the order line to one avoiding to create more
            # than one registration
            so_line.product_uom_qty = 1
            super(SaleOrderLine, so_line)._update_registrations(
                confirm=confirm,
                cancel_to_draft=cancel_to_draft,
                registration_data=registration_data,
            )
            # Set the so line qty back and set the registration qty
            so_line.product_uom_qty = product_uom_qty
            registration = Registration.search(
                [("sale_order_line_id", "=", so_line.id)]
            )
            registration.qty = int(product_uom_qty)
