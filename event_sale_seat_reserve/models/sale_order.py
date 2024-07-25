# Copyright 2024 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0).

from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_draft(self):
        result = super().action_draft()
        self.order_line._set_draft_associated_registrations()
        return result
