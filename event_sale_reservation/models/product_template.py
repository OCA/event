# Copyright 2021 Tecnativa - Jairo Llopis
# Copyright 2023 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models

from ..exceptions import ReservationWithoutEventTypeError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    detailed_type = fields.Selection(
        selection_add=[
            ("event_reservation", "Event Resevation"),
        ],
        ondelete={"event_reservation": "set service"},
    )
    event_reservation_type_id = fields.Many2one(
        comodel_name="event.type",
        index=True,
        string="Event type for reservations",
        help="Type of events that can be reserved by buying this product",
    )

    def _detailed_type_mapping(self):
        type_mapping = super()._detailed_type_mapping()
        type_mapping["event_reservation"] = "service"
        return type_mapping

    @api.constrains("detailed_type")
    def _check_event_reservation(self):
        """Event reservation products checks.

        - A product cannot be both an event ticket and an event reservation.
        - An event reservation must have an event type attached.
        """
        for one in self:
            if one.detailed_type != "event_reservation":
                continue
            if not one.event_reservation_type_id:
                raise ReservationWithoutEventTypeError(
                    _("You must indicate event type for %(name)s.")
                )
