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

    @api.depends("event_reservation_type_id")
    def _compute_product_updatable(self):
        event_registration_lines = self.filtered("event_reservation_type_id")
        # Exclude event registration lines from the computation of product_updatable.
        # If sale_project is installed, this module sets product_updatable to True for
        # service products on confirmed sale orders, preventing the product from being
        # changed when the reservation is converted to an event registration.
        # This workaround allows the product to be changed in that case.
        self -= event_registration_lines
        res = super()._compute_product_updatable()
        event_registration_lines.product_updatable = True
        return res

    @api.depends("event_registration_ids")
    def _compute_event_registration_count(self):
        """Get count of related event registrations."""
        for one in self:
            one.event_registration_count = len(one.event_registration_ids)
