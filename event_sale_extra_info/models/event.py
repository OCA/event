# -*- coding: utf-8 -*-
# © 2016 Antiun Ingeniería S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class EventRegistration(models.Model):
    _inherit = "event.registration"

    commercial_partner_id = fields.Many2one(
        "res.partner",
        "Commercial partner",
        related="partner_id.commercial_partner_id",
        readonly=True,
        store=True,
        help="Commercial partner related to the chosen partner.",
    )
