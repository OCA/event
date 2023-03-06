# Copyright 2017-19 Tecnativa - David Vidal
# Copyright 2021 Moka Tourisme (https://www.mokatourisme.fr).
# @author Iván Todorovich <ivan.todorovich@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class EventRegistration(models.Model):
    _inherit = "event.registration"

    def _synchronize_so_line_values(self, so_line):
        res = super()._synchronize_so_line_values(so_line)
        if so_line:
            res["session_id"] = so_line.event_session_id.id
        return res
