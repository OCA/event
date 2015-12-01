# -*- coding: utf-8 -*-
# © 2015 Antiun Ingeniería, S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class EventEvent(models.Model):
    _inherit = "event.event"

    legal_term_ids = fields.Many2many(
        "website_sale_product_legal.legal_term",
        "website_event_sale_legal_term_event_rel",
        string="Legal terms",
        help="Online customers will be informed of these legal terms before "
             "buying any ticket for this event, in addition to those "
             "specified in the chosen ticket type and product.")


class EventEventTicket(models.Model):
    _inherit = "event.event.ticket"

    legal_term_ids = fields.Many2many(
        "website_sale_product_legal.legal_term",
        "website_event_sale_legal_term_ticket_rel",
        string="Legal terms",
        help="Online customers will be informed of these legal terms before "
             "buying this ticket, in addition to those specified in the "
             "event and in the chosen product.")
    mixed_legal_term_ids = fields.Many2many(
        "website_sale_product_legal.legal_term",
        string="Mixed legal terms",
        compute="_compute_mixed_legal_term_ids",
        help="Combination of legal terms from ticket, event and product.")

    @api.depends("product_id", "event_id", "legal_term_ids")
    def _compute_mixed_legal_term_ids(self):
        for record in self:
            record.mixed_legal_term_ids = (record.legal_term_ids |
                                           record.event_id.legal_term_ids |
                                           record.product_id.legal_term_ids)
