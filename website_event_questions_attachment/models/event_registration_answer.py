# Copyright 2026 INVITU (<https://www.invitu.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class EventRegistrationAnswer(models.Model):
    _inherit = "event.registration.answer"

    value_attachment_id = fields.Many2one(
        "ir.attachment",
        ondelete="set null",
    )

    # Override native constraint to allow attachment as valid answer
    _sql_constraints = [
        (
            "value_check",
            "CHECK("
            "value_answer_id IS NOT NULL"
            " OR COALESCE(value_text_box, '') <> ''"
            " OR value_attachment_id IS NOT NULL"
            ")",
            "There must be a suggested value, a text value, or an attachment.",
        )
    ]
