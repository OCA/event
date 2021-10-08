# Copyright 2021 Camptocamp - Iván Todorovich
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class EventType(models.Model):
    _inherit = "event.type"

    company_id = fields.Many2one("res.company", string="Company", ondelete="cascade",)
