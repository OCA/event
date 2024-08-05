# Copyright 2017 David Vidal<david.vidal@tecnativa.com>
# Copyright 2017 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class EventTrack(models.Model):
    _inherit = "event.event"

    speaker_ids = fields.One2many(
        comodel_name="event.track", compute="_compute_speakers", string="Speakers"
    )

    @api.depends("track_ids.speaker_ids")
    def _compute_speakers(self):
        speakers = []
        for track in self.track_ids:
            speakers += track.speaker_ids
