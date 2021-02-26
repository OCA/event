# Copyright 2016-2017 Tecnativa - Jairo Llopis
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class EventEvent(models.Model):
    _inherit = "event.event"

    city = fields.Char(related="address_id.city", store=True)
