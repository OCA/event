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
        for ticket in self:
            ticket.seats_unconfirmed = (
                ticket.seats_reserved
            ) = ticket.seats_used = ticket.seats_available = 0
        # aggregate registrations by ticket and by state
        results = {}
        if self.ids:
            state_field = {
                "draft": "seats_unconfirmed",
                "reserved": "seats_reserved_unconfirmed",
                "open": "seats_reserved",
                "done": "seats_used",
            }
            query = """ SELECT event_ticket_id, state, count(event_id)
                        FROM event_registration
                        WHERE event_ticket_id IN %s
                        AND state IN ('draft', 'reserved', 'open', 'done') AND active = true
                        GROUP BY event_ticket_id, state
                    """
            self.env["event.registration"].flush_model(
                ["event_id", "event_ticket_id", "state", "active"]
            )
            self.env.cr.execute(query, (tuple(self.ids),))
            for event_ticket_id, state, num in self.env.cr.fetchall():
                results.setdefault(event_ticket_id, {})[state_field[state]] = num

        # compute seats_available
        for ticket in self:
            ticket.update(results.get(ticket._origin.id or ticket.id, {}))
            if ticket.seats_max > 0:
                ticket.seats_available = ticket.seats_max - (
                    ticket.seats_reserved
                    + ticket.seats_used
                    + ticket.seats_reserved_unconfirmed
                )
