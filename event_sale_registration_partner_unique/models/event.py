# -*- coding: utf-8 -*-
# © 2016 Antiun Ingeniería S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, models


class EventRegistration(models.Model):
    _inherit = "event.registration"

    @api.multi
    def _duplicate_search_domain(self):
        """Look for tickets too."""
        result = super(EventRegistration, self)._duplicate_search_domain()
        result.append(("event_ticket_id", "=", self.event_ticket_id.id))
        return result
