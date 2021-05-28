# Copyright 2021 Camptocamp (https://www.camptocamp.com).
# @author Iván Todorovich <ivan.todorovich@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models

from odoo.addons.base.models.res_partner import _lang_get


class EventRegistration(models.Model):
    _inherit = "event.registration"

    lang = fields.Selection(
        selection=_lang_get,
        string="Language",
        compute="_compute_lang",
        readonly=False,
        store=True,
    )

    @api.depends("partner_id")
    def _compute_lang(self):
        for rec in self:
            if rec.partner_id and not rec.lang:
                contact_id = rec.partner_id.address_get().get("contact", False)
                if contact_id:
                    contact = self.env["res.partner"].browse(contact_id)
                    if contact.lang:
                        rec.lang = contact.lang

    @api.model
    def _prepare_attendee_values(self, registration):
        res = super()._prepare_attendee_values(registration)
        if registration.get("lang"):
            res["lang"] = registration["lang"]
        return res
