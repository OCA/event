# Copyright 2025 Tecnativa - Pilar Vargas
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def action_update_event_qty(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "event.sale.update.qty.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_sale_order_line_id": self.id,
                "default_new_qty": self.product_uom_qty,
            },
        }
