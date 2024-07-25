# Copyright 2024 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0).

from odoo import models


class EventRegistration(models.Model):
    _inherit = "event.registration"

    def _need_pre_reservation(self):
        self.ensure_one()

        return self.sale_order_id and self.sale_order_line_id
