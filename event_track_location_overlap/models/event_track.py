# -*- coding: utf-8 -*-
# Copyright 2017 Tecnativa - Jairo Llopis
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from openerp import api, models


class EventTrack(models.Model):
    _inherit = "event.track"

    @api.multi
    @api.constrains("date", "duration", "location_id", "state")
    def _check_location_overlap(self):
        """Make sure no location overlaps happen."""
        self.mapped("location_id")._check_overlappable()
