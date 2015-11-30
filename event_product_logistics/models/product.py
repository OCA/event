# -*- coding: utf-8 -*-
# © 2015 Grupo ESOC Ingeniería de Servicios, S.L.U. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    event_deliverable_product_ids = fields.Many2many(
        "product.product",
        string="Products to deliver in events",
        domain=[("is_event", "=", False)],
        help="These should be delivered to every attendee in any event "
             "related to this product.")
