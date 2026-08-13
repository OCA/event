# Copyright 2025 Tecnativa - Pilar Vargas
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.exceptions import UserError


class EventSaleUpdateQtyWizard(models.TransientModel):
    _name = "event.sale.update.qty.wizard"
    _description = "Wizard to update event attendees quantity from sale order line"

    sale_order_line_id = fields.Many2one("sale.order.line")
    event_id = fields.Many2one(
        related="sale_order_line_id.event_id",
        string="Event",
    )
    ticket_id = fields.Many2one(
        related="sale_order_line_id.event_ticket_id",
        string="Ticket",
    )
    new_qty = fields.Float(
        string="New Quantity",
        required=True,
    )
    registration_ids = fields.Many2many(
        "event.registration",
        string="Attendees",
        domain="[('sale_order_line_id', '=', sale_order_line_id)]",
    )
    show_registrations = fields.Boolean(
        compute="_compute_show_registrations",
    )

    @api.depends("new_qty")
    def _compute_show_registrations(self):
        for wizard in self:
            wizard.show_registrations = (
                wizard.new_qty < wizard.sale_order_line_id.product_uom_qty
            )

    def action_update(self):
        self.ensure_one()
        line = self.sale_order_line_id
        if self.new_qty == line.product_uom_qty:
            raise UserError(self.env._("The quantity has not changed."))
        if self.new_qty < line.product_uom_qty:
            to_remove = self.registration_ids
            if to_remove:
                qty_to_remove = line.product_uom_qty - self.new_qty
                if qty_to_remove != len(to_remove):
                    raise UserError(
                        self.env._(
                            "You must select exactly %s attendee(s) to cancel.",
                            int(qty_to_remove),
                        )
                    )
                to_remove.unlink()
                line.product_uom_qty = self.new_qty
                return {"type": "ir.actions.client", "tag": "soft_reload"}
        if self.new_qty > line.product_uom_qty:
            line.product_uom_qty = self.new_qty
            line._init_registrations()
            result = self.env["ir.actions.act_window"]._for_xml_id(
                "event_sale.action_sale_order_event_registration"
            )
            result["context"] = dict(
                self.env.context,
                default_sale_order_id=line.order_id.id,
                default_sale_order_line_id=line.id,
                event_sale_update_qty=True,
            )
            return result
