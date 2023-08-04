# Copyright 2023 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import _, api, exceptions, fields, models


class EventEvent(models.Model):
    _inherit = "event.event"

    seats_min = fields.Integer(
        string="Minimum Seats",
        compute="_compute_seats_min",
        readonly=False,
        store=True,
        help="For each event you can define a minimum reserved seats (number of "
        "attendees). If it does not reach the mentioned registrations, the event is "
        "highlighted in the list.",
    )

    @api.depends("event_type_id")
    def _compute_seats_min(self):
        for event in self.filtered("event_type_id"):
            event.seats_min = event.event_type_id.default_registration_min

    @api.constrains("seats_min", "seats_max", "seats_limited")
    def _check_seats_min_max(self):
        if any(
            event.seats_limited and event.seats_min > event.seats_max for event in self
        ):
            raise exceptions.ValidationError(
                _(
                    "Maximum attendees number should be greater than minimum attendees "
                    "number."
                )
            )
