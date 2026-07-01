# Copyright 2026 Riccardo Fiore
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.tests.common import TransactionCase


class TestEventCustomRegistration(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.event = cls.env["event.event"].create(
            {
                "name": "Test DJ Night",
                "date_begin": "2099-01-01 20:00:00",
                "date_end": "2099-01-02 02:00:00",
            }
        )

    def _render_registration(self):
        return str(
            self.env["ir.qweb"]._render(
                "website_event.registration_template",
                {
                    "event": self.event,
                    "event_page": True,
                    "cta_additional_classes": "",
                    "registration_error_code": False,
                },
            )
        )

    def test_defaults(self):
        self.assertEqual(self.event.registration_mode, "native")
        self.assertEqual(self.event.external_button_text, "Get Tickets")

    def test_free_mode_renders_message_and_hides_native_labels(self):
        self.event.write(
            {
                "registration_mode": "free",
                "free_event_text": "<p>Free entry, just turn up</p>",
            }
        )
        html = self._render_registration()
        self.assertIn("Free entry, just turn up", html)
        self.assertIn("o_wevent_free_registration", html)
        # No native ticketing chrome leaks through.
        self.assertNotIn("Sold Out", html)
        self.assertNotIn("Registrations <b>Closed</b>", html)

    def test_external_mode_renders_outbound_button(self):
        self.event.write(
            {
                "registration_mode": "external",
                "external_ticket_url": "https://tickets.example.com/dj-night",
                "external_button_text": "Buy on Resident Advisor",
            }
        )
        html = self._render_registration()
        self.assertIn("https://tickets.example.com/dj-night", html)
        self.assertIn("Buy on Resident Advisor", html)
        self.assertIn('target="_blank"', html)
        self.assertNotIn("Sold Out", html)

    def test_native_mode_does_not_leak_custom_markup(self):
        self.event.registration_mode = "native"
        html = self._render_registration()
        self.assertNotIn("o_wevent_free_registration", html)

    def test_closed_event_defaults_to_core_closed_notice(self):
        # Once the event is over, core's "Registrations Closed" notice
        # takes over from the custom content by default.
        self.event.write(
            {
                "date_begin": "2020-01-01 20:00:00",
                "date_end": "2020-01-02 02:00:00",
                "registration_mode": "free",
                "free_event_text": "<p>Free entry, just turn up</p>",
            }
        )
        self.assertFalse(self.event.event_registrations_open)
        html = self._render_registration()
        self.assertNotIn("Free entry, just turn up", html)
        self.assertIn("Closed", html)

    def test_closed_event_keeps_custom_text_when_toggled(self):
        self.event.write(
            {
                "date_begin": "2020-01-01 20:00:00",
                "date_end": "2020-01-02 02:00:00",
                "registration_mode": "free",
                "free_event_text": "<p>Free entry, just turn up</p>",
                "keep_custom_text_when_closed": True,
            }
        )
        html = self._render_registration()
        self.assertIn("Free entry, just turn up", html)
        self.assertNotIn("Closed", html)

    def test_closed_external_event_follows_toggle(self):
        self.event.write(
            {
                "date_begin": "2020-01-01 20:00:00",
                "date_end": "2020-01-02 02:00:00",
                "registration_mode": "external",
                "external_ticket_url": "https://tickets.example.com/dj-night",
            }
        )
        html = self._render_registration()
        self.assertNotIn("https://tickets.example.com/dj-night", html)
        self.assertIn("Closed", html)
        self.event.keep_custom_text_when_closed = True
        html = self._render_registration()
        self.assertIn("https://tickets.example.com/dj-night", html)
        self.assertNotIn("Closed", html)
