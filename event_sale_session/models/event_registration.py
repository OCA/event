# Copyright 2022 Tecnativa - David Vidal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models


class EventRegistration(models.Model):
    _inherit = "event.registration"

    def _synchronize_so_line_values(self, so_line):
        res = super()._synchronize_so_line_values(so_line)
        if so_line:
            res.update({"session_id": so_line.session_id.id})
        return res
