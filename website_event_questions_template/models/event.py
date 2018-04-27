# -*- coding: utf-8 -*-
# Copyright 2017 Tecnativa - Sergio Teruel
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _, fields, models
from odoo.exceptions import UserError


class EventEvent(models.Model):
    _inherit = 'event.event'

    event_question_template_id = fields.Many2one(
        comodel_name='event.question.template',
        string='Questions Template',
    )

    def load_question_template(self):
        # Onchange method is not possible due to
        # https://github.com/odoo/odoo/issues/20163
        self.ensure_one()
        vals = [(6, 0, [])]
        if self.question_ids and self.event_question_template_id:
            raise UserError(_(
                "You can not load a template if there are defined questions"))
        if self.event_question_template_id:
            # Pre-read data for storing values in cache for questions and
            # their answers
            self.event_question_template_id.mapped('question_ids.title')
            self.event_question_template_id.mapped(
                'question_ids.answer_ids.name')
            for question in self.event_question_template_id.question_ids:
                question_vals = question._convert_to_write(question._cache)
                question_vals['answer_ids'] = [
                    (0, 0, x._convert_to_write(x._cache)) for x
                    in question.answer_ids]
                vals.append((0, 0, question_vals))
        self.question_ids = vals
