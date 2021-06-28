# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def update_event_registrations(self):
        for order in self:
            order.order_line._update_registrations(
                confirm=False, cancel_to_draft=False, registration_data=None
            )

        return True

    def confirm_event_registrations(self):
        for sale in self:
            sale.order_line._update_registrations(confirm=True, cancel_to_draft=False)
