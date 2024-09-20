# Copyright 2023 Le Filament (https://le-filament.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import fields, models


class EventQuestion(models.Model):
    _inherit = "event.question"

    question_type = fields.Selection(
        selection_add=[("multiple_choice", "Multiple Selection")],
        ondelete={"multiple_choice": "cascade"},
    )
