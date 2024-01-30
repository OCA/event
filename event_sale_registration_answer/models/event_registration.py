# Copyright (C) 2024 Open Source Integrators (https://www.opensourceintegrators.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models


class EventRegistrationAnswer(models.Model):
    _inherit = "event.registration.answer"

    def _auto_init(self):
        res = super()._auto_init()
        self._cr.execute(
            """ALTER TABLE event_registration_answer
            DROP CONSTRAINT IF EXISTS event_registration_answer_value_check;"""
        )
        return res
