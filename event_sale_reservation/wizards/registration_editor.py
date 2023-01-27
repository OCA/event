# Copyright 2021 Tecnativa - Jairo Llopis
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class RegistrationEditor(models.TransientModel):
    _inherit = "registration.editor"

    @api.model
    def default_get(self, fields):
        """Get data needed to register reservations."""
        result = super().default_get(fields)
        if self.env.context.get("registering_reservations"):
            order = self.env["sale.order"].browse(result["sale_order_id"])
            result["event_registration_ids"] = []
            for sol in order.order_line:
                if sol.product_id.detailed_type != "event_reservation":
                    continue
                sol_type = sol.event_reservation_type_id
                result["event_registration_ids"] += [
                    (
                        0,
                        0,
                        {
                            "sale_order_line_id": sol.id,
                            "event_reservation_type_id": sol_type.id,
                        },
                    )
                ]
        return result

    def action_convert_to_registration(self):
        """Convert reservations to registrations.
        We use the skip_event_sale_registration_multi_qty context to "skip" the
        operation of the event_sale_registration_multi_qty addon because they are
        "incompatible with each other"."""
        # Modify SO lines to be tickets instead of reservations
        for line in self.event_registration_ids:
            line.sale_order_line_id.write(
                {
                    "event_id": line.event_id.id,
                    "event_ticket_id": line.event_ticket_id.id,
                    "product_id": line.event_ticket_id.product_id.id,
                }
            )
        # Close current wizard and reopen normally to configure registrations
        upstream_view = self.env.ref("event_sale.view_event_registration_editor_form")
        return {
            "type": "ir.actions.act_multi",
            "actions": [
                {"type": "ir.actions.act_window_close"},
                {
                    "context": dict(
                        self.env.context,
                        registering_reservations=False,
                        skip_event_sale_registration_multi_qty=True,
                    ),
                    "res_model": self._name,
                    "target": "new",
                    "type": "ir.actions.act_window",
                    "view_id": upstream_view.id,
                    "view_mode": "form",
                    "views": [[upstream_view.id, "form"]],
                },
            ],
        }

    def action_make_registration(self):
        """Force main view reload after finishing."""
        result = super().action_make_registration()
        return {
            "type": "ir.actions.act_multi",
            "actions": [result, {"type": "ir.actions.act_view_reload"}],
        }
