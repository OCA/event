# Copyright 2015 Tecnativa - Javier Iniesta
# Copyright 2016 Tecnativa - Antonio Espinosa
# Copyright 2016 Tecnativa - Vicent Cubells
# Copyright 2018 Jupical Technologies Pvt. Ltd. - Anil Kesariya
# Copyright 2020 Tecnativa - Víctor Martínez
# Copyright 2014-2023 Tecnativa - Pedro M. Baeza
# Copyright 2023 Tecnativa - Carolina Fernandez
# Copyright 2024 Tecnativa - Juan José Seguí
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
        index=True,
    )

    def _prepare_partner(self, vals):
        return {
            "name": vals.get("name") or vals.get("email"),
            "email": vals.get("email", False),
            "phone": vals.get("phone", False),
        }

    def _update_attendee_partner_id(self, vals):
        # Don't update if doing a partner merging
        if (
            not vals.get("attendee_partner_id")
            and vals.get("email")
            and not self.env.context.get("partner_event_merging")
        ):
            Partner = self.env["res.partner"]
            Event = self.env["event.event"]
            # Look for a partner with that email
            email = vals.get("email").replace("%", "").replace("_", "\\_")
            attendee_partner = Partner.search(
                [("email", "=ilike", email)], limit=1, order="id"
            )
            event = Event.browse()
            if vals.get("event_id"):
                event = Event.browse(vals["event_id"])
            if attendee_partner:
                for field in {"name", "phone"}:
                    vals[field] = vals.get(field) or attendee_partner[field]
            elif event and event.create_partner:
                # Create partner
                attendee_partner = Partner.sudo().create(self._prepare_partner(vals))
            vals["attendee_partner_id"] = attendee_partner.id
        return vals

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            self._update_attendee_partner_id(vals)
        return super().create(vals_list)

    def write(self, vals):
        self._update_attendee_partner_id(vals)
        return super().write(vals)

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
            self = self.with_context(**get_attendee_partner_address)
            for registration in self:
                if registration.partner_id:
                    vals = registration._synchronize_partner_values(
                        registration.partner_id
                    )
                    # On Odoo 19.0 "mobile" field is removed
                    # https://github.com/odoo/odoo/pull/189739
                    # so this should not be ported to 19.0+
                    if "mobile" not in registration._fields and "mobile" in vals:
                        mobile = vals.pop("mobile")
                        phone = vals.get("phone") or mobile
                        if phone:
                            vals["phone"] = phone
                    registration.update(vals)
        return {}
