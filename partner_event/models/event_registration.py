# Copyright 2014 Tecnativa S.L. - Pedro M. Baeza
# Copyright 2015 Tecnativa S.L. - Javier Iniesta
# Copyright 2016 Tecnativa S.L. - Antonio Espinosa
# Copyright 2016 Tecnativa S.L. - Vicent Cubells
# Copyright 2020 Tecnativa S.L. - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class EventRegistration(models.Model):
    _inherit = "event.registration"

    partner_id = fields.Many2one(ondelete="restrict")
    attendee_partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Attendee Partner",
        ondelete="restrict",
        copy=False,
    )

    def _prepare_partner(self, vals):
        return {
            "name": vals.get("name") or vals.get("email"),
            "email": vals.get("email", False),
            "phone": vals.get("phone", False),
        }

    @api.model_create_multi
    def create(self, vals_list):
        for values in vals_list:
            if not values.get("attendee_partner_id") and values.get("email"):
                Partner = self.env["res.partner"]
                Event = self.env["event.event"]
                # Look for a partner with that email
                email = values.get("email").replace("%", "").replace("_", "\\_")
                attendee_partner = Partner.search([("email", "=ilike", email)], limit=1)
                event = Event.browse(values["event_id"])
                if attendee_partner:
                    for field in {"name", "phone", "mobile"}:
                        values[field] = values.get(field) or attendee_partner[field]
                elif event.create_partner:
                    # Create partner
                    attendee_partner = Partner.sudo().create(
                        self._prepare_partner(values)
                    )
                values["attendee_partner_id"] = attendee_partner.id
        return super(EventRegistration, self).create(vals_list)

    def partner_data_update(self, data):
        reg_data = {k: v for k, v in data.items() if k in ["name", "email", "phone"]}
        if reg_data:
            # Only update registration data if this event is not old
            registrations = self.filtered(
                lambda x: x.event_end_date >= fields.Datetime.now()
            )
            registrations.write(reg_data)

    @api.onchange("attendee_partner_id", "partner_id")
    def _onchange_partner_id(self):
        if self.attendee_partner_id:
            if not self.partner_id:
                self.partner_id = self.attendee_partner_id
            get_attendee_partner_address = {
                "get_attendee_partner_address": self.attendee_partner_id,
            }
            return super(
                EventRegistration, self.with_context(**get_attendee_partner_address)
            )._onchange_partner_id()
        return super(EventRegistration, self)._onchange_partner_id()
