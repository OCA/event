# Copyright 2016 Tecnativa - Jairo Llopis
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests.common import HttpCase, tagged


@tagged("post_install", "-at_install")
class UICase(HttpCase):
    def test_ui_website(self):
        """Test frontend tour."""
        self.start_tour("/event", "website_event_filter_city", login="portal")
