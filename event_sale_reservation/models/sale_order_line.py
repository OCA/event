# Copyright 2021 Tecnativa - Jairo Llopis
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    event_registration_ids = fields.One2many(
        comodel_name="event.registration",
        inverse_name="sale_order_line_id",
        string="Event registrations",
        help="Event registrations related to this sale order line",
    )
    event_registration_count = fields.Integer(
        compute="_compute_event_registration_count",
        store=True,
        help="Count of event registrations related to this sale order line",
    )
    event_reservation_type_id = fields.Many2one(
        index=True,
        readonly=True,
        related="product_id.event_reservation_type_id",
        store=True,
    )

    @api.depends("event_registration_ids")
    def _compute_event_registration_count(self):
        """Get count of related event registrations."""
        for one in self:
            one.event_registration_count = len(one.event_registration_ids)
