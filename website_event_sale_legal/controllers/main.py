# -*- coding: utf-8 -*-
# © 2015 Antiun Ingeniería, S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, http


class EventLegalTerms(http.Controller):
    @http.route(
        "/website_event_sale_legal/<model('event.event.ticket'):ticket>",
        type="http", auth="public", website=True)
    def by_ticket(self, ticket):
        """Get legal terms by event ticket."""
        if ticket.mixed_legal_term_ids:
            return http.request.website.render(
                "website_sale_product_legal.legal_terms",
                self._render_values(ticket))
        else:
            raise http.request.NotFound()

    def _render_values(self, ticket):
        """Values to render the legal_terms template."""
        return {
            "additional_title":
                _("Legal terms to buy %(ticket)s ticket for event %(event)s") %
                {"ticket": ticket.name_get()[0][1],
                 "event": ticket.event_id.name_get()[0][1]},
            "legal_terms": ticket.mixed_legal_term_ids,
            "product": ticket.product_id,
            "ticket": ticket,
        }
