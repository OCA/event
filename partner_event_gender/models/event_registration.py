# Copyright 2026 INVITU (<https://www.invitu.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class EventRegistration(models.Model):
    _inherit = "event.registration"

    gender = fields.Selection(
        [("male", "Male"), ("female", "Female"), ("other", "Other")]
    )

    @api.onchange("attendee_partner_id", "partner_id")
    def _onchange_partner_id(self):
        res = super()._onchange_partner_id()
        for registration in self:
            if registration.attendee_partner_id:
                registration.gender = registration.attendee_partner_id.gender
        return res

    @api.model
    def _prepare_partner(self, vals):
        res = super()._prepare_partner(vals)
        res["gender"] = vals.get("gender") or False
        return res
