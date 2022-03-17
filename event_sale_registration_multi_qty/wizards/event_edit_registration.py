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
            return super().default_get(fields)
        Event = self.env["event.event"]
        SaleOrderLine = self.env["sale.order.line"]
        event_multi_records_dict = {}
        registrations = res.get("event_registration_ids", [])
        filtered_registrations = []
        for registration in registrations:
            if len(registration) != 3:
                filtered_registrations.append(registration)
                continue
            event = Event.browse(registration[2].get("event_id"))
            so_line = SaleOrderLine.browse(registration[2].get("sale_order_line_id"))
            if not event.registration_multi_qty:
                filtered_registrations.append(registration)
                continue
            event_line_key = (event, so_line)
            # Drop subsequent records which we won't use
            if event_multi_records_dict.get(event_line_key):
                continue
            registration[2].update({"qty": so_line.product_uom_qty})
            event_multi_records_dict[event_line_key] = registration
            filtered_registrations.append(registration)
        res["event_registration_ids"] = filtered_registrations
        return res


class RegistrationEditorLine(models.TransientModel):
    _inherit = "registration.editor.line"

    qty = fields.Integer(string="Quantity", default=1)

    def get_registration_data(self):
        res = super().get_registration_data()
        res["qty"] = self.qty
        return res
