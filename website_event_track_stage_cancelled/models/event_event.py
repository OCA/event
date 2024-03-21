# Copyright 2024 Tecnativa S.L. - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class EventEvent(models.Model):
    _inherit = "event.event"

    def button_cancel(self):
        """Perform cancellation of the sessions"""
        res = super().button_cancel()
        stage_id = self.env["event.track.stage"].search(
            [("is_cancel", "=", True)], limit=1
        )
        if stage_id:
            self.track_ids.stage_id = stage_id
        return res
