# Copyright 2020 Studio73 - Ioan Galan
# Copyright 2023 Tecnativa - Carolina Fernandez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from dateutil.relativedelta import relativedelta

from odoo import fields
from odoo.tests import HttpCase


class TestTicket(HttpCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        now = fields.Datetime.now()
        cls.website = cls.env["website"].browse(1)
        cls.event_question_free_text = "Free Text"
        cls.event_1 = cls.env["event.event"].create(
            {
                "name": "Event One",
                "user_id": cls.env.ref("base.user_admin").id,
                "date_begin": now + relativedelta(days=1),
                "date_end": now + relativedelta(days=3),
                "organizer_id": cls.env.ref("base.res_partner_1").id,
                "event_type_id": cls.env.ref("event.event_type_1").id,
                "website_published": True,
                "description": "Test",
                "auto_confirm": True,
                "website_id": cls.website.id,
            }
        )
        cls.ticket_1 = cls.env["event.event.ticket"].create(
            {"name": "Ticket One", "event_id": cls.event_1.id}
        )
        cls.ticket_2 = cls.env["event.event.ticket"].create(
            {"name": "Ticket Two", "event_id": cls.event_1.id}
        )
        cls.question_1 = cls.env["event.question"].create(
            {
                "title": "Question Two",
                "event_id": cls.event_1.id,
                "restricted_ticket_ids": [(6, 0, cls.ticket_1.ids)],
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
