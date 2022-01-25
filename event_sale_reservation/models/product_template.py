# Copyright 2021 Tecnativa - Jairo Llopis
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models

from ..exceptions import ReservationWithoutEventTypeError, TicketAndReservationError


class Product(models.Model):
    _inherit = "product.template"

    event_reservation_ok = fields.Boolean(
        index=True,
        string="Is an event reservation",
        help=(
            "If checked, this product enables selling event reservations "
            "even before an event of the specified type has been scheduled."
        ),
    )
    event_reservation_type_id = fields.Many2one(
        comodel_name="event.type",
        index=True,
        string="Event type for reservations",
        help="Type of events that can be reserved by buying this product",
    )

    @api.constrains("event_ok", "event_reservation_ok")
    def _check_event_reservation(self):
        """Event reservation products checks.

        - A product cannot be both an event ticket and an event reservation.
        - An event reservation must have an event type attached.
        """
        for one in self:
            if not one.event_reservation_ok:
                continue
            if one.event_ok:
                raise TicketAndReservationError(
                    _(
                        "Product %(name)s cannot be both an event ticket and "
                        "an event reservation."
                    )
                    % {"name": one.display_name}
                )
            if not one.event_reservation_type_id:
                raise ReservationWithoutEventTypeError(
                    _("You must indicate event type for %(name)s.")
                )
