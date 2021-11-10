# Copyright 2017 Tecnativa - Sergio Teruel
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class TemplateEventQuestion(models.Model):
    _name = "event.question.template"
    _description = "Event questions template"

    name = fields.Char(required=True)
    question_ids = fields.One2many(
        comodel_name="event.question.template.question",
        inverse_name="template_id",
        required=True,
        string="Questions",
    )


class EventQuestionTemplateQuestion(models.Model):
    _inherit = "event.question"
    _name = "event.question.template.question"
    _description = "Questions for event template"

    # Field not required for a template
    event_id = fields.Many2one(required=False)
    answer_ids = fields.One2many(
        comodel_name="event.question.template.answer",
        inverse_name="question_id",
        string="Answers",
        required=True,
    )
    template_id = fields.Many2one(
        comodel_name="event.question.template",
        string="Event Question Template",
        required=True,
        ondelete="cascade",
    )


class EventQuestionTemplateAnswer(models.Model):
    _inherit = "event.question.answer"
    _name = "event.question.template.answer"
    _description = "Answers for question template"
    _order = "sequence,id"

    question_id = fields.Many2one(
        comodel_name="event.question.template.question",
        required=True,
        ondelete="cascade",
    )
