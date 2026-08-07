# Copyright 2016 Tecnativa - Jairo Llopis
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests.common import HttpCase, new_test_user, tagged


@tagged("post_install", "-at_install")
class UICase(HttpCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        websites = cls.env["website"].search([])
        # Activate country filters in all websites
        for website in websites:
            cls.env.ref("website_event.event_location").with_context(
                website_id=website.id
            ).active = True
        location = cls.env["res.partner"].create(
            {
                "name": "Tenerife Auditorium",
                "street": "Av. de la Constitución, 1",
                "city": "Santa Cruz de Tenerife",
                "zip": "38003",
                "country_id": cls.env.ref("base.es").id,
            }
        )
        event = cls.env["event.event"].create(
            {
                "name": "My Event Test",
                "date_begin": "2026-09-15 10:00:00",
                "date_end": "2026-09-15 18:00:00",
                "date_tz": "Atlantic/Canary",
                "user_id": cls.env.user.id,
                "address_id": location.id,
            }
        )
        event.website_published = True
        cls.user = new_test_user(
            cls.env,
            login="test-user",
            name="test user",
            email="testuser@test.com",
            groups="base.group_portal",
            password="testuser",
        )

    def test_ui_website(self):
        """Test frontend tour."""
        self.start_tour("/event", "website_event_filter_city", login="test-user")
