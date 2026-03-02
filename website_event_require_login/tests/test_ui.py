# Copyright 2026 TechnoLibre - Mathieu Benoit
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import date, timedelta

from odoo import fields
from odoo.tests import new_test_user, tagged
from odoo.tests.common import HttpCase


@tagged("post_install", "-at_install")
class TestWebsiteEventRequireLoginUI(HttpCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.event = cls.env["event.event"].create(
            {
                "name": "Test Event Require Login Tour",
                "date_begin": fields.Date.to_string(date.today()),
                "date_end": fields.Date.to_string(date.today() + timedelta(days=7)),
                "website_published": True,
                "website_require_login": True,
            }
        )
        cls.ticket = cls.env["event.event.ticket"].create(
            {
                "name": "Standard",
                "event_id": cls.event.id,
                "seats_max": 100,
            }
        )
        cls.portal_user = new_test_user(
            cls.env,
            login="portal_event_login",
            groups="base.group_portal",
            password="portal_event_login",
            name="Portal Event User",
        )

    def test_public_user_sees_login_modal(self):
        """Public user clicks Register and the login-required modal
        appears instead of the attendee form."""
        self.start_tour(
            "/event",
            "website_event_require_login_public",
            step_delay=100,
        )

    def test_authenticated_user_normal_flow(self):
        """Authenticated portal user clicks Register and the normal
        attendee registration form appears (no login modal)."""
        self.start_tour(
            "/event",
            "website_event_require_login_auth",
            login="portal_event_login",
            step_delay=100,
        )
