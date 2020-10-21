# Copyright 2020 Studio73 - Ioan Galan
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from dateutil.relativedelta import relativedelta

from odoo import fields, http
from odoo.tests import HttpCase

from odoo.addons.website.tools import MockRequest


class TestFreeText(HttpCase):
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
                "question_ids": [(0, 0, {"title": "Question One", "free_text": True})],
            }
        )

    def test_free_text_answer(self):
        with MockRequest(self.env, website=self.website):
            self.confirm(self.event_1)
            self.assertEqual(
                self.event_1.registration_ids.free_answer_ids.answer,
                self.event_question_free_text,
            )
        return True

    def test_free_text_display_name(self):
        with MockRequest(self.env, website=self.website):
            self.confirm(self.event_1)
            display_name = "{}: {}".format(
                self.event_1.question_ids.title, self.event_question_free_text
            )
            self.assertEqual(
                self.event_1.registration_ids.free_answer_ids.display_name, display_name
            )
        return True

    def confirm(self, event):
        self.authenticate("demo", "demo")
        self.url_open(
            "/event/{}/registration/confirm".format(event.id),
            data=self._build_confirmation_req_values(event),
        )
        return True

    def _build_confirmation_req_values(self, event):
        values = self._prepare_registration_confirm_values(event)
        values["csrf_token"] = http.WebRequest.csrf_token(self)
        return values

    def _prepare_registration_confirm_values(self, event, counter=1, ticket_id=0):
        return {
            "{}-name".format(counter): "Test",
            "{}-email".format(counter): "test@test.com",
            "{}-ticket_id".format(counter): ticket_id,
            "{}-answer_free_text-{}".format(
                ticket_id, event.question_ids.id
            ): self.event_question_free_text,
        }
