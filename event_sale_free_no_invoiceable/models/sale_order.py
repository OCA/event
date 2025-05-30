# Copyright 2025 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models
from odoo.tools import float_is_zero


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _compute_qty_to_invoice(self):
        precision = self.env["decimal.precision"].precision_get(
            "Product Unit of Measure"
        )
        event_zero_lines = self.filtered(
            lambda x: x.event_ticket_id
            and float_is_zero(x.price_unit, precision_digits=precision)
        )
        event_zero_lines.qty_to_invoice = 0
        self = self - event_zero_lines
        return super()._compute_qty_to_invoice()
