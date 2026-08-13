# Copyright 2026 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

from odoo.tests.common import HttpCase

from odoo.addons.website.tools import MockRequest

from ..controllers.main import WebsiteEventController


class TestWebsiteEventSaleRegistrationMultiQty(HttpCase):
    def setUp(self):
        super().setUp()
        self.authenticate(None, None)
        self.event = self.env.ref(
            "website_event_sale_registration_multi_qty.multi_qty_event"
        )
        self.website = self.env.ref("website.default_website")
        self.controller = WebsiteEventController()

    def test_multi_qty_registration_no_tickets(self):
        """
        Test that a multi quantity registration via the website
        creates a registration with that quantity
        """
        with MockRequest(self.env, website=self.website):
            data = {
                "use_multi_qty-0": "42",
                "1-name": "testname",
                "1-email": "test@test.com",
                "1-event_ticket_id": "0",
            }
            registration_data = self.controller._process_attendees_form(
                self.event, data
            )
            self.controller._create_attendees_from_registration_post(
                self.event, registration_data
            )

        self.assertEqual(self.event.registration_ids.qty, 42)

    def test_multi_qty_registration_with_tickets(self):
        """
        Test that a multi quantity registration via the website
        creates a registration with that quantity, and a simultaneous
        registration with the normal flow creates registrations with qty 1
        """
        ticket1 = self.env["event.event.ticket"].create(
            {
                "name": "ticket1",
                "event_id": self.event.id,
            }
        )
        ticket2 = self.env["event.event.ticket"].create(
            {
                "name": "ticket2",
                "event_id": self.event.id,
            }
        )
        with MockRequest(self.env, website=self.website):
            data = {
                f"use_multi_qty-{ticket1.id}": "3",
                "1-name": "testname",
                "1-email": "test@test.com",
                "1-event_ticket_id": str(ticket1.id),
                "4-name": "testname",
                "4-email": "test@test.com",
                "4-event_ticket_id": str(ticket2.id),
                "5-name": "testname",
                "5-email": "test@test.com",
                "5-event_ticket_id": str(ticket2.id),
            }
            registration_data = self.controller._process_attendees_form(
                self.event, data
            )
            registrations = self.controller._create_attendees_from_registration_post(
                self.event, registration_data
            )

        self.assertEqual(self.event.registration_ids[0].qty, 1)
        self.assertEqual(self.event.registration_ids[1].qty, 1)
        self.assertEqual(self.event.registration_ids[2].qty, 3)
        self.assertEqual(registrations[0].sale_order_line_id.product_uom_qty, 3)
        self.assertEqual(registrations[1].sale_order_line_id.product_uom_qty, 2)
