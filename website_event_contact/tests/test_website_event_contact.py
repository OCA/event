# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import Command
from odoo.tests.common import HttpCase, tagged


@tagged("post_install", "-at_install")
class TestWebsiteEventContact(HttpCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.contact = cls.env["res.partner"].create(
            {"name": "Event Contact Person", "function": "Event manager"}
        )
        cls.event = cls.env["event.event"].create(
            {
                "name": "Event with contacts",
                "date_begin": "2030-06-20 10:00:00",
                "date_end": "2030-06-23 18:00:00",
                "date_tz": "Europe/Madrid",
                "website_published": True,
                "contact_ids": [Command.set(cls.contact.ids)],
            }
        )
        cls.view = cls.env.ref("website_event_contact.website_event_contact_details")

    def test_contacts_hidden_by_default(self):
        """The contact section is an inactive view, so visitors do not see it."""
        response = self.url_open(self.event.website_url)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(self.contact.name, response.text)

    def test_contacts_shown_when_view_is_active(self):
        """Enabling the option shows the event contacts on the event page."""
        self.view.active = True
        response = self.url_open(self.event.website_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.contact.name, response.text)
