# Copyright 2017-19 Tecnativa - David Vidal
# Copyright 2017 Tecnativa - Sergio Teruel
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class RegistrationEditor(models.TransientModel):
    _inherit = "registration.editor"

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        if self.env.context.get("skip_event_sale_registration_multi_qty"):
            return res
        Event = self.env["event.event"]
        SaleOrderLine = self.env["sale.order.line"]
        attendees = [(6, 0, [])]
        attendees_no_multi = []
        so_line_id = False
        registration = (
            res["event_registration_ids"] and res["event_registration_ids"][0]
        )
        if registration:
            multi_qty = Event.browse(registration[2]["event_id"]).registration_multi_qty
            if multi_qty:
                if registration[2]["sale_order_line_id"] != so_line_id:
                    so_line_id = registration[2]["sale_order_line_id"]
                    so_line = SaleOrderLine.browse(so_line_id)
                    if multi_qty:
                        registration[2].update({"qty": so_line.product_uom_qty})
                        attendees.append(registration)
            else:
                registration[2].update({"qty": 1})
                attendees_no_multi.append(registration)
        if len(attendees) > 1:
            attendees.extend(attendees_no_multi)
            res["event_registration_ids"] = attendees
        return res


class RegistrationEditorLine(models.TransientModel):
    _inherit = "registration.editor.line"

    qty = fields.Integer(string="Quantity", default=1)

    def get_registration_data(self):
        res = super().get_registration_data()
        res["qty"] = self.qty
        return res
