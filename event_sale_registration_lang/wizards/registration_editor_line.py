# Copyright 2021 Camptocamp (https://www.camptocamp.com).
# @author Iván Todorovich <ivan.todorovich@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models

from odoo.addons.base.models.res_partner import _lang_get


class RegistrationEditorLine(models.TransientModel):
    _inherit = "registration.editor.line"

    lang = fields.Selection(selection=_lang_get, string="Language",)

    def get_registration_data(self):
        res = super().get_registration_data()
        res["lang"] = self.lang or self.editor_id.sale_order_id.partner_id.lang
        return res
