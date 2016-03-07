# -*- coding: utf-8 -*-
# © 2016 Antiun Ingeniería S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models
from .. import exceptions


class EventEvent(models.Model):
    _inherit = "event.event"

    forbid_duplicates = fields.Boolean(
        help="Check this to disallow duplicate partners in this event's "
             "registrations",
    )

    @api.multi
    @api.constrains("forbid_duplicates", "registration_ids")
    def _check_forbid_duplicates(self):
        """Ensure no duplicated partners are found in the event."""
        return (self.filtered("forbid_duplicates")
                .registration_ids._check_forbid_duplicates())


class EventRegistration(models.Model):
    _inherit = "event.registration"

    @api.multi
    @api.constrains("event_id", "partner_id")
    def _check_forbid_duplicates(self):
        """Ensure no duplicated partners are found in the event."""
        for s in self.filtered("event_id.forbid_duplicates"):
            dupes = self.search(s._duplicate_search_domain())
            if dupes:
                raise exceptions.DuplicatedPartnerError(
                    s.event_id.display_name,
                    ", ".join(d.display_name
                              for d in dupes.mapped("partner_id")),
                    registrations=dupes,
                )

    @api.multi
    def _duplicate_search_domain(self):
        """What to look for when searching duplicates."""
        return [
            ("id", "!=", self.id),
            ("event_id", "=", self.event_id.id),
            ("partner_id", "=", self.partner_id.id),
        ]
