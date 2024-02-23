# Copyright (C) 2024 Open Source Integrators (https://www.opensourceintegrators.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models


class EventRegistration(models.Model):
    _inherit = "event.registration"

    def _prepare_event_reg_answer_vals(self, question):
        return {
            "registration_id": self.id,
            "question_id": question.id,
        }

    def populate_answers(self):
        EventRegAnswer = self.env["event.registration.answer"]
        for registration in self:
            questions = registration.event_id.question_ids
            if registration != registration.event_id.registration_ids[0]:
                questions = questions.filtered(lambda x: not x.once_per_order)
            existing = registration.registration_answer_ids.question_id
            missing = questions - existing
            for question in missing:
                answer_vals = registration._prepare_event_reg_answer_vals(question)
                EventRegAnswer.create(answer_vals)
        return self.registration_answer_ids
