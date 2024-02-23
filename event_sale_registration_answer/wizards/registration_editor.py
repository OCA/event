# Copyright (C) 2024 Open Source Integrators (https://www.opensourceintegrators.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models


class RegistrationEditor(models.TransientModel):
    _inherit = "registration.editor"

    def action_make_registration(self):
        res = super().action_make_registration()
        self.ensure_one()
        # If there are answer to populate, open the list after the Registrations popup
        answers = self.sale_order_id.registration_ids.registration_answer_ids
        if answers:
            res = self.sale_order_id.action_view_questions_list()
        return res
