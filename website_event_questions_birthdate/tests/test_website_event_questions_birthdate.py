# Copyright 2026 INVITU (<https://www.invitu.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from datetime import datetime

from odoo.tests.common import TransactionCase


class TestWebsiteEventQuestionsBirthdate(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.event = cls.env["event.event"].create(
            {
                "name": "Test Event",
                "date_begin": datetime(2026, 9, 1, 8, 0),
                "date_end": datetime(2026, 9, 1, 18, 0),
            }
        )

    def test_birthdate_date_in_allowed_fields(self):
        """birthdate_date is in website registration allowed fields."""
        allowed = self.env[
            "event.registration"
        ]._get_website_registration_allowed_fields()
        self.assertIn("birthdate_date", allowed)

    def test_birthdate_date_question_type_exists(self):
        """birthdate_date is available as a question type."""
        question = self.env["event.question"].create(
            {
                "title": "Birth Date",
                "question_type": "birthdate_date",
                "event_id": self.event.id,
            }
        )
        self.assertEqual(question.question_type, "birthdate_date")
