# Copyright 2017 David Vidal<david.vidal@tecnativa.com>
# Copyright 2017 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class EventTrackDate(models.Model):
    _name = "event.track.date"
    _description = "Track dates"

    track_id = fields.Many2one("event.track")
    date = fields.Datetime()
