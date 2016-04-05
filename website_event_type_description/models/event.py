# -*- coding: utf-8 -*-
# © 2016 Antiun Ingeniería S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class EventType(models.Model):
    _inherit = "event.type"

    description = fields.Html(
        help="Description for this event, as showin in the website.")
