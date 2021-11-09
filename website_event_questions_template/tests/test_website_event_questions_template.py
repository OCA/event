# Copyright 2017 Tecnativa - Sergio Teruel
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.exceptions import UserError
from odoo.tests.common import SavepointCase


class EventQuestionTemplate(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(EventQuestionTemplate, cls).setUpClass()
        cls.template1 = cls.env["event.question.template"].create(
            {
                "name": "Template test 01",
            }
        )
        cls.template2 = cls.env["event.question.template"].create(
            {
                "name": "Template test 01",
                "question_ids": [
                    (
                        0,
                        0,
                        {
                            "title": "question T2 01",
                            "once_per_order": True,
                            "answer_ids": [
                                (0, 0, {"name": "Answer 01 test 01"}),
                                (0, 0, {"name": "Answer 02 test 01"}),
                            ],
                        },
                    )
                ],
            }
        )

    def test_event_template(self):
        # Create an event
        vals = {
            "name": "Event test",
            "date_begin": "2017-05-01",
            "date_end": "2017-06-01",
            "auto_confirm": False,
            "event_question_template_id": self.template1.id,
        }
        event = self.env["event.event"].create(vals)
        event._onchange_event_question_template_id()
        self.assertFalse(
            event.question_ids,
            "Event Question Template: Questions created for this event",
        )

        # Change template in event
        event.event_question_template_id = self.template2
        event._onchange_event_question_template_id()
        self.assertEqual(
            len(event.question_ids), 1, "Event Question Template: Questions only one"
        )

        self.assertEqual(
            len(event.question_ids.answer_ids), 2, "Event Question Template: Answer two"
        )

    def test_event_template_not_allowed(self):
        """Create an event with two questions, if I load the template raise
        error
        """
        vals = {
            "name": "Event test",
            "date_begin": "2017-05-01",
            "date_end": "2017-06-01",
            "auto_confirm": False,
            "event_question_template_id": self.template2.id,
            "question_ids": [
                (
                    0,
                    0,
                    {
                        "title": "question T2 01",
                        "once_per_order": True,
                    },
                ),
                (
                    0,
                    0,
                    {
                        "title": "question T2 02",
                        "once_per_order": True,
                    },
                ),
            ],
        }
        event = self.env["event.event"].create(vals)
        with self.assertRaises(UserError):
            event._onchange_event_question_template_id()
