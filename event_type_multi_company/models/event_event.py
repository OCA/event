# Copyright 2021 Camptocamp - Iván Todorovich
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class EventEvent(models.Model):
    _inherit = "event.event"
    _check_company_auto = True

    event_type_id = fields.Many2one(check_company=True)
