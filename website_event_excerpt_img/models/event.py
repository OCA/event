# -*- coding: utf-8 -*-
# © 2016 Antiun Ingeniería S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class EventEvent(models.Model):
    _inherit = "event.event"

    priority = fields.Selection(
        [("0", "Normal"), ("1", "Highlighted")],
        required=True,
        default="0",
        help="Importance of the event, as shown in website (if enabled).")
