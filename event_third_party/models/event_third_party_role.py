# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class EventThirdPartyRole(models.Model):

    _name = "event.third.party.role"
    _description = "Event Third Party Role"

    name = fields.Char(
        required=True,
        translate=True,
        index=True,
    )
    color = fields.Integer()

    @api.model
    def _get_role_colors(self):
        """
        These are variables defined in o-colors (in web/) but not accessible
        from base model.
        """
        return [
            "#000000",
            "#F06050",
            "#F4A460",
            "#F7CD1F",
            "#6CC1ED",
            "#814968",
            "#EB7E7F",
            "#2C8397",
            "#475577",
            "#D6145F",
            "#30C381",
            "#9365B8",
        ]
