# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import fields, models


class EventTrack(models.Model):
    _inherit = "event.track"

    speaker_ids = fields.Many2many(
        comodel_name="event.track.speaker", string="Speakers"
    )
