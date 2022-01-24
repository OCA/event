# Copyright 2017 Tecnativa - Jairo Llopis
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import api, models


class EventTrack(models.Model):
    _inherit = "event.track"

    @api.constrains("date", "duration", "location_id", "stage_id")
    def _check_location_overlap(self):
        """Make sure no location overlaps happen."""
        for location in self.mapped("location_id"):
            location._check_overlappable_one()
