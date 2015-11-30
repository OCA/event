# -*- coding: utf-8 -*-
# © 2015 Antiun Ingeniería, S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class LegalTerm(models.Model):
    _inherit = "website_sale_product_legal.legal_term"

    event_ids = fields.Many2many(
        "event.event",
        "website_event_sale_legal_term_event_rel",
        string="Events",
        help="Events that require accepting this legal term.")
