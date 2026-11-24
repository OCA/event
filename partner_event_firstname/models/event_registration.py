# Copyright 2026 INVITU (<https://www.invitu.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, models


class EventRegistration(models.Model):
    _inherit = "event.registration"

    @api.onchange("attendee_partner_id", "partner_id")
    def _onchange_partner_id(self):
        res = super()._onchange_partner_id()
        for registration in self:
            if registration.attendee_partner_id:
                registration.firstname = registration.attendee_partner_id.firstname
                registration.lastname = registration.attendee_partner_id.lastname
        return res

    @api.model
    def _prepare_partner(self, vals):
        res = super()._prepare_partner(vals)
        firstname = vals.get("firstname") or False
        lastname = vals.get("lastname") or False
        res["firstname"] = firstname
        res["lastname"] = lastname
        if firstname or lastname:
            res["name"] = self._get_name(lastname, firstname)
        return res
