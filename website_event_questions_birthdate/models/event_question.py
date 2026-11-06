# Copyright 2026 INVITU (<https://www.invitu.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class EventQuestion(models.Model):
    _inherit = "event.question"

    question_type = fields.Selection(
        selection_add=[("birthdate_date", "Birth Date")],
        ondelete={"birthdate_date": "cascade"},
    )
