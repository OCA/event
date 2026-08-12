# Copyright 2021 Tecnativa - Jairo Llopis
# Copyright 2023 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models

from ..exceptions import ReservationWithoutEventTypeError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    service_tracking = fields.Selection(
        selection_add=[
            ("event_reservation", "Event Reservation"),
        ],
        ondelete={"event_reservation": "set default"},
    )
    event_reservation_type_id = fields.Many2one(
        comodel_name="event.type",
        index=True,
        string="Event type for reservations",
        help="Type of events that can be reserved by buying this product",
    )

    @api.constrains("service_tracking", "event_reservation_type_id")
    def _check_event_reservation(self):
        """Event reservation products checks.

        - A product cannot be both an event ticket and an event reservation.
        - An event reservation must have an event type attached.
        """
        for one in self:
            if one.service_tracking != "event_reservation":
                continue
            if not one.event_reservation_type_id:
                raise ReservationWithoutEventTypeError(
                    self.env._("You must indicate event type for %(name)s.")
                )

    @api.onchange("service_tracking")
    def _onchange_service_tracking_event_reservation(self):
        if self.service_tracking == "event_reservation":
            self.type = "service"
            self.invoice_policy = "order"
