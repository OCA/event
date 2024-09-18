# Copyright 2017 David Vidal<david.vidal@tecnativa.com>
# Copyright 2017 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class EventTrackEquipmentLine(models.Model):
    _name = "event.track.equipment.line"
    _description = "Track Equipments Line"

    track_id = fields.Many2one("event.track", string="Track")
    equipment_id = fields.Many2one("event.track.equipment", string="Equipment")
    quantity = fields.Integer(default=1)

    _sql_constraints = [
        (
            "event_track_equipment_line_equipment_uniq",
            "unique (track_id, equipment_id)",
            "Duplicate equipments on a track is not allowed, modify "
            "quantity of existing line.",
        )
    ]
