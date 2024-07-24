# Copyright 2024 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0).
from odoo import api, fields, models


class EventEvent(models.Model):
    _inherit = "event.event"

    seats_reserved_unconfirmed = fields.Integer(
        string="Number of Reserved Attendees",
        store=False,
        readonly=True,
        compute="_compute_seats",
    )

    @api.depends("seats_max", "registration_ids.state", "registration_ids.active")
    def _compute_seats(self):
        # Override the original method to add the new state and the compute for the new field
        # initialize fields to 0
        for event in self:
            event.seats_unconfirmed = (
                event.seats_reserved_unconfirmed
            ) = event.seats_reserved = event.seats_used = event.seats_available = 0
        # aggregate registrations by event and by state
        state_field = {
            "draft": "seats_unconfirmed",
            "reserved": "seats_reserved_unconfirmed",
            "open": "seats_reserved",
            "done": "seats_used",
        }
        base_vals = {fname: 0 for fname in state_field.values()}
        results = {event_id: dict(base_vals) for event_id in self.ids}
        if self.ids:
            query = """ SELECT event_id, state, count(event_id)
                        FROM event_registration
                        WHERE event_id IN %s
                        AND state IN ('draft', 'reserved', 'open', 'done') AND active = true
                        GROUP BY event_id, state
                    """
            self.env["event.registration"].flush_model(["event_id", "state", "active"])
            self._cr.execute(query, (tuple(self.ids),))
            res = self._cr.fetchall()
            for event_id, state, num in res:
                results[event_id][state_field[state]] = num

        # compute seats_available and expected
        for event in self:
            event.update(results.get(event._origin.id or event.id, base_vals))
            if event.seats_max > 0:
                event.seats_available = event.seats_max - (
                    event.seats_reserved
                    + event.seats_used
                    + event.seats_reserved_unconfirmed
                )

            event.seats_expected = (
                event.seats_unconfirmed
                + event.seats_reserved_unconfirmed
                + event.seats_reserved
                + event.seats_used
            )
