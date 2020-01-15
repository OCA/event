# Copyright 2016 Tecnativa. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class EventType(models.Model):
    _inherit = "event.type"

    description = fields.Html(
        help="Description for this type of event, as showing in the website.")
