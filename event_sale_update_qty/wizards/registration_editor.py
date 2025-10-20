# Copyright 2025 Tecnativa - Pilar Vargas
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import Command, api, models


class RegistrationEditor(models.TransientModel):
    _inherit = "registration.editor"

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        order_line_id = self.env.context.get("default_sale_order_line_id")
        if not self.env.context.get("event_sale_update_qty") or not order_line_id:
            return res
        order_line = self.env["sale.order.line"].browse(order_line_id)
        new_registrations = order_line.registration_ids.filtered(
            lambda reg: reg.state == "draft"
        )
        res["event_registration_ids"] = [
            Command.create(
                {
                    "event_id": reg.event_id.id,
                    "event_ticket_id": reg.event_ticket_id.id,
                    "registration_id": reg.id,
                    "name": reg.name,
                    "email": reg.email,
                    "phone": reg.phone,
                    "sale_order_line_id": order_line.id,
                },
            )
            for reg in new_registrations
        ]
        return res
