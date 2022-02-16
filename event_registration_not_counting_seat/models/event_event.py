# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)

from odoo import api, models


class Event(models.Model):
    _inherit = "event.event"

    @api.onchange("event_type_id")
    def _onchange_type(self):
        super()._onchange_type()

        if self.event_type_id.use_ticketing:
            for type_ticket in self.event_type_id.event_ticket_ids:
                ticket = self.event_ticket_ids.filtered(
                    lambda t: t.product_id == type_ticket.product_id
                    and t.price == type_ticket.price
                )
                if ticket:
                    ticket.count_seat = type_ticket.count_seat

    @api.depends("seats_max", "registration_ids.state")
    def _compute_seats(self):
        """ complete override"""
        for event in self:
            event.seats_unconfirmed = (
                event.seats_reserved
            ) = event.seats_used = event.seats_available = 0
        # aggregate registrations by event and by state
        if self.ids:
            state_field = {
                "draft": "seats_unconfirmed",
                "open": "seats_reserved",
                "done": "seats_used",
            }
            query = """ SELECT event_id, state, count(event_id)
                        FROM event_registration
                        WHERE event_id IN %s AND state IN ('draft', 'open', 'done')
                            AND count_seat
                        GROUP BY event_id, state
                    """
            self.env["event.registration"].flush(["event_id", "state"])
            self._cr.execute(query, (tuple(self.ids),))
            for event_id, state, num in self._cr.fetchall():
                event = self.browse(event_id)
                event[state_field[state]] += num
        # compute seats_available
        for event in self:
            if event.seats_max > 0:
                event.seats_available = event.seats_max - (
                    event.seats_reserved + event.seats_used
                )
            event.seats_expected = (
                event.seats_unconfirmed + event.seats_reserved + event.seats_used
            )
