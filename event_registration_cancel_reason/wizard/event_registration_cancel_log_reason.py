# Copyright 2016 Tecnativa - Pedro M. Baeza
# Copyright 2017 Tecnativa - Vicent Cubells
# Copyright 2020 Tecnativa - Víctor Martínez
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import _, api, exceptions, fields, models


class EventRegistrationCancelLogReason(models.TransientModel):
    _name = "event.registration.cancel.log.reason"
    _description = "Event Registration Cancel Log Reason"

    event_type_id = fields.Many2one(comodel_name="event.type", string="Event type")
    reason_id = fields.Many2one(
        comodel_name="event.registration.cancel.reason",
        required=True,
        domain="['|', "
        " ('event_type_ids', '=', False), "
        " ('event_type_ids', '=', event_type_id)]",
    )

    @api.model
    def default_get(self, var_fields):
        res = super(EventRegistrationCancelLogReason, self).default_get(var_fields)
        registrations = self.env["event.registration"].browse(
            self.env.context["active_ids"]
        )
        first_type = registrations[:1].event_id.event_type_id
        for event in registrations.mapped("event_id"):
            if event.event_type_id != first_type:
                raise exceptions.ValidationError(
                    _(
                        "You cannot cancel registrations from events of "
                        "different types at once."
                    )
                )
        res["event_type_id"] = first_type.id
        return res

    def button_log(self):
        self.ensure_one()
        registrations = self.env["event.registration"].browse(
            self.env.context["active_ids"]
        )
        registrations.write({"cancel_reason_id": self.reason_id.id})
        registrations.with_context(bypass_reason=True).action_cancel()
