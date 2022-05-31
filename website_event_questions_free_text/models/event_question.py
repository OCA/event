# Copyright 2019 Tecnativa - Pedro M. Baeza
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class EventQuestion(models.Model):
    _inherit = "event.question"

    free_text = fields.Boolean(help="Allow user to introduce a free text as answer.")
