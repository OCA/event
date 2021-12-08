# Copyright 2017-19 Tecnativa - David Vidal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class EventSession(models.Model):
    _inherit = "event.session"

    order_line_ids = fields.One2many(
        comodel_name="sale.order.line",
        inverse_name="session_id",
        string="Sales Order Lines",
    )
    unconfirmed_qty = fields.Integer(
        string="Unconfirmed Qty",
        compute="_compute_unconfirmed_qty",
        store=True,
    )

    @api.depends(
        "order_line_ids",
        "order_line_ids.product_uom_qty",
        "order_line_ids.order_id.state",
    )
    def _compute_unconfirmed_qty(self):
        for session in self:
            session.unconfirmed_qty = int(
                sum(
                    session.order_line_ids.filtered(
                        lambda x: x.order_id.state in ("draft", "sent")
                    ).mapped("product_uom_qty")
                )
            )
