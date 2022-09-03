# Copyright 2020 Studio73 - Ioan Galan
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from dateutil.relativedelta import relativedelta

from odoo import fields
from odoo.tests import HttpCase


class TestTicket(HttpCase):
    def setUp(self):
        super().setUp()
        now = fields.Datetime.now()
        self.website = self.env["website"].browse(1)
        self.event_question_free_text = "Free Text"
        self.event_1 = self.env["event.event"].create(
            {
                "name": "Event One",
                "user_id": self.env.ref("base.user_admin").id,
                "date_begin": now + relativedelta(days=1),
                "date_end": now + relativedelta(days=3),
                "organizer_id": self.env.ref("base.res_partner_1").id,
                "event_type_id": self.env.ref("event.event_type_1").id,
                "website_published": True,
                "description": "Test",
                "auto_confirm": True,
                "website_id": self.website.id,
            }
        )
        self.ticket_1 = self.env["event.event.ticket"].create(
            {"name": "Ticket One", "event_id": self.event_1.id}
        )
        self.ticket_2 = self.env["event.event.ticket"].create(
            {"name": "Ticket Two", "event_id": self.event_1.id}
        )
        self.question_1 = self.env["event.question"].create(
            {
                "title": "Question Two",
                "event_id": self.event_1.id,
                "restricted_ticket_ids": [(6, 0, self.ticket_1.ids)],
            }
        )

    def test_specific_questions(self):
        specific_questions = self.event_1._get_specific_questions(self.ticket_1.id)
        self.assertTrue(self.question_1 in specific_questions)
        return True

    def test_general_questions(self):
        general_questions = self.event_1._get_general_questions(self.ticket_2.ids)
        self.assertFalse(self.question_1 in general_questions)
        return True
