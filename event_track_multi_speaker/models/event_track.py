# Copyright 2017 David Vidal<david.vidal@tecnativa.com>
# Copyright 2017 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class EventTrack(models.Model):
    _inherit = "event.track"

    speaker_ids = fields.Many2many(
        comodel_name="event.track.speaker", string="Speakers"
    )
