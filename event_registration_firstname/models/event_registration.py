# Copyright 2026 INVITU (<https://www.invitu.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class EventRegistration(models.Model):
    _inherit = "event.registration"

    firstname = fields.Char()
    lastname = fields.Char()

    @api.model
    def _get_name(self, lastname, firstname):
        """Compute name from parts using partner_firstname names order config."""
        return self.env["res.partner"]._get_computed_name(lastname, firstname)

    @api.onchange("firstname", "lastname")
    def _onchange_firstname_lastname(self):
        if self.firstname or self.lastname:
            self.name = self._get_name(self.lastname, self.firstname)

    def _prepare_vals_on_create_firstname_lastname(self, vals):
        if vals.get("firstname") or vals.get("lastname"):
            vals["name"] = self._get_name(vals.get("lastname"), vals.get("firstname"))
        elif vals.get("name"):
            parts = self.env["res.partner"]._get_inverse_name(vals["name"])
            vals["lastname"] = parts.get("lastname")
            vals["firstname"] = parts.get("firstname")

    def _prepare_vals_on_write_firstname_lastname(self, vals):
        if "firstname" in vals or "lastname" in vals:
            lastname = vals.get("lastname", self.lastname)
            firstname = vals.get("firstname", self.firstname)
            vals["name"] = self._get_name(lastname, firstname)
        elif vals.get("name"):
            parts = self.env["res.partner"]._get_inverse_name(vals["name"])
            vals["lastname"] = parts.get("lastname")
            vals["firstname"] = parts.get("firstname")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            self._prepare_vals_on_create_firstname_lastname(vals)
        return super().create(vals_list)

    def write(self, vals):
        self._prepare_vals_on_write_firstname_lastname(vals)
        return super().write(vals)
