# Copyright 2021 Tecnativa - Jairo Llopis
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class RegistrationEditorLine(models.TransientModel):
    _inherit = "registration.editor.line"

    event_reservation_type_id = fields.Many2one(
        related="sale_order_line_id.event_reservation_type_id",
        readonly=True,
    )
