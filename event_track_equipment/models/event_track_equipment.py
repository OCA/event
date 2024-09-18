# Copyright 2017 David Vidal<david.vidal@tecnativa.com>
# Copyright 2017 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class EventTrackEquipment(models.Model):
    _name = "event.track.equipment"
    _description = "Track Equipments"

    name = fields.Char()
