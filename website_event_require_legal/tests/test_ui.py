# Copyright 2025 Tecnativa - Pilar Vargas
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import date, timedelta

from odoo import fields
from odoo.tests import new_test_user, tagged
from odoo.tests.common import HttpCase


@tagged("post_install", "-at_install")
class TestWebsiteEventRequireLegal(HttpCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.organizer = cls.env["res.partner"].create({"name": "Organizer"})
        cls.date = {
            "begin": fields.Date.to_string(date.today()),
            "end": fields.Date.to_string(date.today() + timedelta(days=7)),
        }
        cls.event = cls.env["event.event"].create(
            {
                "name": "Test event for require legal",
                "date_begin": cls.date["begin"],
                "date_end": cls.date["end"],
                "website_require_legal": True,
                "website_description_legal": "Test description legal",
                "is_published": True,
            }
        )
        cls.user = new_test_user(
            cls.env,
            login="super_mario",
            groups="base.group_portal",
            password="super_mario",
            name="Super Mario",
        )

    def test_ui_website(self):
        """Test frontend tour."""
        self.start_tour(
            "/event",
            "website_event_require_legal",
            login="super_mario",
            step_delay=100,
        )
        registration = self.env["event.registration"].search(
            [("name", "=", "Super Mario")]
        )
        # Assert that the registration have metadata logs
        self.assertTrue(
            registration.message_ids.filtered(
                lambda one: "Website legal terms acceptance metadata" in one.body
            )
        )
