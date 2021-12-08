# Copyright 2017-19 Tecnativa - David Vidal
# Copyright 2021 Moka Tourisme (https://www.mokatourisme.fr).
# @author Iván Todorovich <ivan.todorovich@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class RegistrationEditor(models.TransientModel):
    _inherit = "registration.editor"

    @api.model
    def default_get(self, fields):
        # OVERRIDE to fill in the session_id for existing and new registration vals
        # If the registration already exists, we get it from the registration itself
        # If the registration doesn't exist, we get it from the sale order line
        res = super().default_get(fields)
        for __, __, attendee_vals in res["event_registration_ids"]:
            registration_id = attendee_vals.get("registration_id")
            if registration_id:
                registration = self.env["event.registration"].browse(registration_id)
                attendee_vals["session_id"] = registration.session_id.id
            else:
                sale_order_line_id = attendee_vals.get("sale_order_line_id")
                sale_order_line = self.env["sale.order.line"].browse(sale_order_line_id)
                attendee_vals["session_id"] = sale_order_line.event_session_id.id
        return res


class RegistrationEditorLine(models.TransientModel):
    _inherit = "registration.editor.line"

    session_id = fields.Many2one(comodel_name="event.session", string="Session")

    def get_registration_data(self):
        res = super().get_registration_data()
        res["session_id"] = self.sale_order_line_id.event_session_id.id
        return res
