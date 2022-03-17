# Copyright 2017-19 Tecnativa - David Vidal
# Copyright 2017 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _compute_attendee_count(self):
        """Adapt registrations counter to multi quantity"""
        super()._compute_attendee_count()
        event = self.env["event.event"].search(
            [
                ("sale_order_lines_ids", "in", self.order_line.ids),
                ("registration_multi_qty", "=", True),
            ]
        )
        multi_qty_regs = self.env["event.registration"].search_read(
            [
                ("sale_order_id", "in", self.ids),
                ("state", "!=", "cancel"),
                ("event_id", "in", event.ids),
            ],
            ["sale_order_id", "qty"],
        )
        attendee_count_data = {}
        for registration in multi_qty_regs:
            attendee_count_data.setdefault(registration["sale_order_id"][0], 0)
            # We minorate 1 as it's already count in super() by every registration
            attendee_count_data[registration["sale_order_id"][0]] += (
                registration["qty"] - 1
            )
        for sale_order in self:
            sale_order.attendee_count += attendee_count_data.get(sale_order.id, 0)


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _update_registrations(
        self,
        confirm=True,
        cancel_to_draft=False,
        registration_data=None,
        mark_as_paid=False,
    ):
        """Update registrations on events with multi qty enabled"""
        if self.env.context.get("skip_event_sale_registration_multi_qty"):
            return super()._update_registrations(
                confirm=confirm,
                cancel_to_draft=cancel_to_draft,
                registration_data=registration_data,
                mark_as_paid=mark_as_paid,
            )
        Registration = self.env["event.registration"].sudo()
        for so_line in self.filtered("event_id"):
            if not so_line.event_id.registration_multi_qty:
                super(SaleOrderLine, so_line)._update_registrations(
                    confirm=confirm,
                    cancel_to_draft=cancel_to_draft,
                    registration_data=registration_data,
                    mark_as_paid=mark_as_paid,
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
                mark_as_paid=mark_as_paid,
            )
            # Set the so line qty back and set the registration qty
            so_line.product_uom_qty = product_uom_qty
            registration = Registration.search(
                [("sale_order_line_id", "=", so_line.id)]
            )
            registration.qty = int(product_uom_qty)
