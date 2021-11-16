# Copyright 2016 Antiun Ingeniería S.L. - Jairo Llopis
# Copyright 2020 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models

from .. import exceptions


class EventEvent(models.Model):
    _inherit = "event.event"

    forbid_duplicates = fields.Boolean(
        help="Check this to disallow duplicate attendees in this event's "
        "registrations",
    )

    @api.constrains("forbid_duplicates", "registration_ids")
    def _check_forbid_duplicates(self):
        """Ensure no duplicated attendee are found in the event."""
        return self.filtered(
            "forbid_duplicates"
        ).registration_ids._check_forbid_duplicates()


class EventRegistration(models.Model):
    _inherit = "event.registration"

    @api.constrains("event_id", "attendee_partner_id")
    def _check_forbid_duplicates(self):
        """Ensure no duplicated attendees are found in the event."""
        for event_reg in self.filtered("event_id.forbid_duplicates"):
            dupes = self.search(event_reg._duplicate_search_domain())
            if dupes:
                raise exceptions.DuplicatedPartnerError(
                    event_reg.event_id.display_name,
                    ", ".join(
                        partner_id.display_name
                        for partner_id in dupes.mapped("attendee_partner_id")
                    ),
                    registrations=dupes,
                )

    def _duplicate_search_domain(self):
        """What to look for when searching duplicates."""
        return [
            ("id", "!=", self.id),
            ("event_id", "=", self.event_id.id),
            ("attendee_partner_id", "=", self.attendee_partner_id.id),
            ("attendee_partner_id", "!=", False),
        ]
