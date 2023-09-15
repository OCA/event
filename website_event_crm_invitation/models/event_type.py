# Copyright 2021 Tecnativa - Jairo Llopis
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class EventType(models.Model):
    _inherit = "event.type"

    def _published_events_domain(self):
        """Get domain for open and published events of this category."""
        domain = self._events_domain()
        domain += [
            ("date_begin", ">", fields.Datetime.now()),
            ("website_published", "=", True),
            "|",
            ("seats_limited", "=", False),
            ("seats_available", ">", 0),
        ]
        return domain
