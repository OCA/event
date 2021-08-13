# Copyright 2020 Studio73 - Ioan Galan
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from dateutil.relativedelta import relativedelta

from odoo import fields
from odoo.tests import SavepointCase
from odoo.tools.misc import mute_logger

from odoo.addons.website.tools import MockRequest

from ..controllers.main import WebsiteEvent


class TestFreeText(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        now = fields.Datetime.now()
        cls.user_demo = cls.env.ref("base.user_demo")
        cls.website_event_controller = WebsiteEvent()
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
                "question_ids": [(0, 0, {"title": "Question One", "free_text": True})],
            }
        )

    def test_free_text_answer(self):
        self.confirm(self.event_1)
        self.assertEqual(
            self.event_1.registration_ids.free_answer_ids.answer,
            self.event_question_free_text,
        )

    def test_free_text_display_name(self):
        self.confirm(self.event_1)
        display_name = "{}: {}".format(
            self.event_1.question_ids.title, self.event_question_free_text
        )
        self.assertEqual(
            self.event_1.registration_ids.free_answer_ids.display_name, display_name
        )

    # HACK https://github.com/odoo/odoo/issues/75061
    @mute_logger("odoo.http")
    def confirm(self, event):
        with MockRequest(self.env(user=self.user_demo), website=self.website):
            self.website_event_controller.registration_confirm(
                event, **self._prepare_registration_confirm_values(event)
            )

    def _prepare_registration_confirm_values(self, event, counter=1, ticket_id=0):
        return {
            "{}-name".format(counter): "Test",
            "{}-email".format(counter): "test@test.com",
            "{}-ticket_id".format(counter): ticket_id,
            "{}-answer_free_text-{}".format(
                ticket_id, event.question_ids.id
            ): self.event_question_free_text,
        }
