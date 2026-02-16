# Copyright 2026 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import odoo
from odoo import fields
from odoo.tests import HOST
from odoo.tests.common import HttpCase, tagged


@tagged("post_install", "-at_install")
class TestWebsiteEventRibbon(HttpCase):
    def setUp(self):
        super().setUp()
        self.ribbon = self.env["event.event.ribbon"].create(
            {
                "name": "Test Ribbon",
                "bg_color": "#FF0000",
                "text_color": "#00FF00",
                "position": "right",
            }
        )
        self.event = self.env["event.event"].create(
            {
                "name": "Test Event",
                "date_begin": fields.Datetime.now(),
                "date_end": fields.Datetime.now(),
                "website_ribbon_id": self.ribbon.id,
                "website_published": True,
            }
        )

    def test_event_ribbon_display(self):
        """Test that the event ribbon is displayed correctly on the event page."""
        response = self.opener.get(
            f"http://{HOST}:{odoo.tools.config['http_port']}/event"
        )
        self.assertEqual(response.status_code, 200)
        # Check that the ribbon's name is in the response
        self.assertIn(self.ribbon.name, response.text)
        # Check that the ribbon's style is in the response
        expected_style = (
            f"background-color: {self.ribbon.bg_color}; "
            f"color: {self.ribbon.text_color};"
        )
        self.assertIn(expected_style, response.text)
        # Check that the ribbon's position class is in the response
        expected_class = "o_ribbon_right"
        self.assertIn(expected_class, response.text)
