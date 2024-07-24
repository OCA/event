# Copyright 2024 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0).
from odoo import api, fields, models


class EventTicket(models.Model):
    _inherit = "event.event.ticket"

    seats_reserved_unconfirmed = fields.Integer(
        string="Number of Reserved Attendees", compute="_compute_seats"
    )

    @api.depends("seats_max", "registration_ids.state", "registration_ids.active")
    def _compute_seats(self):
        """Determine reserved, available, reserved but unconfirmed and used seats."""
        # initialize fields to 0 + compute seats availability
        res = super()._compute_seats()
        counts = dict()
        if self.ids:
            groups = self.env["event.registration"].read_group(
                [
                    ("event_ticket_id", "in", self.ids),
                    ("state", "=", "reserved"),
                ],
                groupby=["event_ticket_id"],
                fields=["event_ticket_id"],
            )
            counts = {
                g["event_ticket_id"][0]: g["event_ticket_id_count"] for g in groups
            }

        # compute seats_available
        for ticket in self:
            ticket.seats_reserved_unconfirmed = counts.get(ticket.id, 0)
            if ticket.seats_max > 0:
                ticket.seats_available = ticket.seats_max - (
                    ticket.seats_reserved
                    + ticket.seats_used
                    + ticket.seats_reserved_unconfirmed
                )
        return res
