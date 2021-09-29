# Copyright 2021 Camptocamp (https://www.camptocamp.com).
# @author Iván Todorovich <ivan.todorovich@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class RegistrationEditor(models.TransientModel):
    _inherit = "registration.editor"

    @api.model
    def default_get(self, fields):
        # When popuplating the registration.editor.line values from
        # existing registrations, populate also their lang
        res = super().default_get(fields)
        if "event_registration_ids" in res:
            for __, __, reg_vals in res["event_registration_ids"]:
                if "registration_id" in reg_vals:
                    registration = self.env["event.registration"].browse(
                        reg_vals["registration_id"]
                    )
                    reg_vals["lang"] = registration.lang
        return res
