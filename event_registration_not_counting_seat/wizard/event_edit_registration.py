# Copyright 2022 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)

from odoo import models


class RegistrationEditorLine(models.TransientModel):
    """Event Registration"""

    _inherit = "registration.editor.line"

    def get_registration_data(self):
        self.ensure_one()
        res = super().get_registration_data()
        # update count_seat boolean from ticket
        res["count_seat"] = self.event_ticket_id.count_seat
        return res
