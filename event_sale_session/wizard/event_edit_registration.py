# Copyright 2017-19 Tecnativa - David Vidal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class RegistrationEditor(models.TransientModel):
    _inherit = "registration.editor"

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        so_line = self.env["sale.order.line"]
        for registration in res["event_registration_ids"]:
            if so_line.id != registration[2]["sale_order_line_id"]:
                so_line = so_line.browse(registration[2]["sale_order_line_id"])
                registration[2]["session_id"] = so_line.session_id.id
        return res


class RegistrationEditorLine(models.TransientModel):
    """Event Registration"""

    _inherit = "registration.editor.line"

    session_id = fields.Many2one(comodel_name="event.session", string="Session")

    def get_registration_data(self):
        res = super().get_registration_data()
        res.update({"session_id": self.sale_order_line_id.session_id.id})
        return res
