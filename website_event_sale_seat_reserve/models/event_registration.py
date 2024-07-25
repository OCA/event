# Copyright 2024 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0).

from odoo import api, models


class EventRegistration(models.Model):
    _inherit = "event.registration"

    def _auto_reserve_registrations(self):
        to_reserve = self.filtered(
            lambda rec: (
                rec.state == "draft" and rec.sale_order_line_id and rec.visitor_id
            )
        )
        to_reserve.action_set_reserved()

    @api.model_create_multi
    def create(self, vals_list):
        registrations = super().create(vals_list)
        registrations._auto_reserve_registrations()
        return registrations
