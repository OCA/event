# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class EventEvent(models.Model):

    _inherit = "event.event"

    third_party_ids = fields.One2many(
        comodel_name="event.third.party",
        inverse_name="event_id",
    )
