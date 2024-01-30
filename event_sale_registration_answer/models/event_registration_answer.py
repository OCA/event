# Copyright (C) 2024 Open Source Integrators (https://www.opensourceintegrators.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class EventRegistrationAnswer(models.Model):
    _inherit = "event.registration.answer"

    def _auto_init(self):
        res = super()._auto_init()
        # To be able to prepopulate empty answers,
        # we need to drop the requires answer check
        self._cr.execute(
            """ALTER TABLE event_registration_answer
            DROP CONSTRAINT IF EXISTS event_registration_answer_value_check;"""
        )
        return res

    once_per_order = fields.Boolean(related="question_id.once_per_order", store=True)
