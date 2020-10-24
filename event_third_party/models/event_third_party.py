# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class EventThirdParty(models.Model):

    _name = "event.third.party"
    _description = "Third Party"
    _rec_name = "partner_id"

    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Partner",
        ondelete="restrict",
        required=True,
        index=True,
    )
    event_id = fields.Many2one(
        comodel_name="event.event",
        string="Event",
        ondelete="cascade",
        required=True,
        index=True,
    )
    role_ids = fields.Many2many(
        comodel_name="event.third.party.role",
        string="Roles",
    )
