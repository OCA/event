# Copyright 2021 Tecnativa - Jairo Llopis
# Copyright 2025 Tecnativa - Pilar Vargas
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models
from odoo.osv import expression


class EventType(models.Model):
    _inherit = "event.type"

    def _published_events_domain(self):
        """Get domain for open and published events of this category."""
        base_domain = self._events_domain()
        base_domain += [
            ("date_begin", ">", fields.Datetime.now()),
            ("website_published", "=", True),
        ]
        domain = base_domain + [
            ("seats_limited", "=", False),
        ]
        # Search limited events with available seats (not storable)
        events_with_seats = self.env["event.event"].search(
            base_domain
            + [
                ("seats_limited", "=", True),
            ]
        )
        valid_event_ids = events_with_seats.filtered(
            lambda e: e.seats_available > 0
        ).ids
        if valid_event_ids:
            domain = expression.OR(
                [
                    domain,
                    [("id", "in", valid_event_ids)],
                ]
            )
        return domain
