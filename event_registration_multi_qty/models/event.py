# Copyright 2017 Tecnativa - Sergio Teruel
# Copyright 2017 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class EventEvent(models.Model):
    _inherit = "event.event"

    registration_multi_qty = fields.Boolean(
        string="Allow multiple attendees per registration", default=True,
    )

    @api.depends("seats_max", "registration_ids.state", "registration_ids.qty")
    def _compute_seats(self):
        multi_qty_events = self.filtered("registration_multi_qty")
        for event in multi_qty_events:
            vals = {
                "seats_unconfirmed": 0,
                "seats_reserved": 0,
                "seats_used": 0,
                "seats_available": 0,
            }
            registrations = self.env["event.registration"].read_group(
                [
                    ("event_id", "=", event.id),
                    ("state", "in", ["draft", "open", "done"]),
                ],
                ["state", "qty"],
                ["state"],
            )
            for registration in registrations:
                if registration["state"] == "draft":
                    vals["seats_unconfirmed"] += registration["qty"]
                elif registration["state"] == "open":
                    vals["seats_reserved"] += registration["qty"]
                elif registration["state"] == "done":
                    vals["seats_used"] += registration["qty"]
            if event.seats_max > 0:
                vals["seats_available"] = event.seats_max - (
                    vals["seats_reserved"] + vals["seats_used"]
                )
            vals["seats_expected"] = (
                vals["seats_unconfirmed"] + vals["seats_reserved"] + vals["seats_used"]
            )
            event.update(vals)
        rest = self - multi_qty_events
        super(EventEvent, rest)._compute_seats()

    @api.constrains("registration_multi_qty")
    def _check_attendees_qty(self):
        for event in self:
            if (
                not event.registration_multi_qty
                and max(event.registration_ids.mapped("qty") or [0]) > 1
            ):
                raise ValidationError(
                    _(
                        "You can not disable this option if there are "
                        "registrations with quantities greater than one."
                    )
                )


class EventRegistration(models.Model):
    _inherit = "event.registration"

    qty = fields.Integer(string="Quantity", required=True, default=1,)

    @api.constrains("qty")
    def _check_attendees_qty(self):
        for registration in self:
            if (
                not registration.event_id.registration_multi_qty
                and registration.qty > 1
            ):
                raise ValidationError(
                    _(
                        "You can not add quantities if you not active the"
                        ' option "Allow multiple attendees per registration"'
                        " in event"
                    )
                )

    @api.model
    def _prepare_attendee_values(self, registration):
        res = super()._prepare_attendee_values(registration)
        # Passed fields are not taken into account if a default is set,
        # so we need to force this
        if "qty" in registration:
            res.update({"qty": registration.get("qty")})
        return res
