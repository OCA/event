# Copyright 2019 Tecnativa - Pedro M. Baeza
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class EventRegistration(models.Model):
    _inherit = 'event.registration'

    free_answer_ids = fields.One2many(
        comodel_name='event.answer.free',
        inverse_name='registration_id',
        string='Free Answers',
    )


class EventQuestion(models.Model):
    _inherit = 'event.question'

    free_text = fields.Boolean(
        help="Allow user to introduce a free text as answer."
    )


class EventAnswerFree(models.Model):
    _name = 'event.answer.free'
    _description = 'Event Answer Free Text'

    registration_id = fields.Many2one(
        comodel_name='event.registration',
        required=True,
        ondelete="cascade",
    )
    question_id = fields.Many2one(
        comodel_name='event.question',
        required=True,
        ondelete="restrict",
        domain="[('free_text', '=', True)]",
    )
    answer = fields.Char(
        required=True,
    )

    _sql_constraints = [
        ('unique_registration_question',
         'UNIQUE(registration_id, question_id)',
         "You can't answer the same question 2 times"),
    ]

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, "%s: %s" % (
                record.question_id.title,
                record.answer,
            )))
        return result
