# Copyright 2021 Camptocamp SA - Iván Todorovich
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import re

from lxml import etree

from odoo.tests import HttpCase, tagged


@tagged("-at_install", "post_install")
class TestEventSalePortal(HttpCase):
    def setUp(self):
        super().setUp()
        self.customer = self.env.ref("base.res_partner_3")
        self.product_event = self.env.ref("event_sale.product_product_event")
        # Create demo event
        self.event = self.env["event.event"].create(
            {
                "name": "Test Portal Event",
                "date_begin": "2022-06-20",
                "date_end": "2022-06-23",
                "portal_badge_download": True,
            }
        )
        # Create tickets
        self.ticket_adults = self.env["event.event.ticket"].create(
            {
                "name": "Adults",
                "product_id": self.product_event.id,
                "event_id": self.event.id,
                "price": 15.00,
            }
        )
        self.ticket_kids = self.env["event.event.ticket"].create(
            {
                "name": "Kids",
                "product_id": self.product_event.id,
                "event_id": self.event.id,
                "price": 5.00,
            }
        )

    def test_01_sale_order_portal(self):
        # Create sale order
        order = self.env["sale.order"].create(
            {
                "partner_id": self.customer.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.product_event.id,
                            "name": "Event registration",
                            "event_id": self.event.id,
                            "event_ticket_id": self.ticket_adults.id,
                            "price_unit": 15.00,
                            "product_uom_qty": 1,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "product_id": self.product_event.id,
                            "name": "Event registration",
                            "event_id": self.event.id,
                            "event_ticket_id": self.ticket_kids.id,
                            "price_unit": 5.00,
                            "product_uom_qty": 2,
                        },
                    ),
                ],
            }
        )
        # Confirm order and registrations
        order.action_confirm()
        order.order_line._update_registrations(confirm=True)
        # Get portal url
        res = self.url_open(order._get_share_url())
        self.assertEqual(res.status_code, 200)
        root = etree.fromstring(res.content, etree.HTMLParser())
        # Check that we have registrations
        section = root.xpath("//section[@id='event_registrations']")
        self.assertEqual(
            len(section), 1, "We should have the event registrations section"
        )
        # Check that we have the download button
        buttons = root.xpath(
            "//section[@id='event_registrations']"
            "//td[@name='td_actions']"
            "//a[hasclass('download')]"
        )
        self.assertEqual(len(buttons), 3)
        # Check that we can download a single registration
        href = buttons[0].attrib["href"]
        res = self.url_open(href)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers["Content-Type"], "application/pdf")
        # Check that we can download all event badges at once
        button = root.xpath(
            "//section[@id='event_registrations']//div//a[@title='Download all']"
        )
        self.assertEqual(len(button), 1, "We should have a Download all button")
        href = button[0].attrib["href"]
        res = self.url_open(href)
        res = self.url_open(order._get_share_url())
        self.assertEqual(res.status_code, 200)
        root = etree.fromstring(res.content, etree.HTMLParser())

    def test_02_sale_order_portal_no_download(self):
        # Disable badge downloading on event
        self.event.portal_badge_download = False
        # Create sale order
        order = self.env["sale.order"].create(
            {
                "partner_id": self.customer.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.product_event.id,
                            "name": "Event registration",
                            "event_id": self.event.id,
                            "event_ticket_id": self.ticket_adults.id,
                            "price_unit": 15.00,
                            "product_uom_qty": 1,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "product_id": self.product_event.id,
                            "name": "Event registration",
                            "event_id": self.event.id,
                            "event_ticket_id": self.ticket_kids.id,
                            "price_unit": 5.00,
                            "product_uom_qty": 2,
                        },
                    ),
                ],
            }
        )
        # Confirm order and registrations
        order.action_confirm()
        order.order_line._update_registrations(confirm=True)
        # Get portal url
        res = self.url_open(order._get_share_url())
        self.assertEqual(res.status_code, 200)
        root = etree.fromstring(res.content, etree.HTMLParser())
        # Check that we have registrations
        section = root.xpath("//section[@id='event_registrations']")
        self.assertEqual(
            len(section), 1, "We should have the event registrations section"
        )
        # Check that we aren't able to download registrations
        buttons = root.xpath(
            "//section[@id='event_registrations']"
            "//td[@name='td_actions']"
            "//a[hasclass('download')]"
        )
        self.assertEqual(len(buttons), 0)
        # Check that we can't download all event badges at once
        button = root.xpath(
            "//section[@id='event_registrations']//div//a[@title='Download all']"
        )
        self.assertEqual(len(button), 0)

    def test_02_sale_order_no_registrations(self):
        # Create sale order
        order = self.env["sale.order"].create({"partner_id": self.customer.id})
        order.action_confirm()
        # Get portal url
        res = self.url_open(order._get_share_url())
        self.assertEqual(res.status_code, 200)
        root = etree.fromstring(res.content, etree.HTMLParser())
        # Check that we don't have registrations
        section = root.xpath("//section[@id='event_registrations']")
        self.assertEqual(
            len(section), 0, "We shouldn't have any event registrations section"
        )

    def test_03_sale_order_wrong_token_errors(self):
        # Create sale order
        order = self.env["sale.order"].create(
            {
                "partner_id": self.customer.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.product_event.id,
                            "name": "Event registration",
                            "event_id": self.event.id,
                            "event_ticket_id": self.ticket_adults.id,
                            "price_unit": 15.00,
                            "product_uom_qty": 1,
                        },
                    ),
                ],
            }
        )
        # Confirm order and registrations
        order.action_confirm()
        order.order_line._update_registrations(confirm=True)
        # Get portal url
        order_url = order._get_share_url()
        # Case 1: Attempt a to access with a different token
        wrong_token_url = re.sub(r"(?<=access_token=)([^&]+)", "something", order_url,)
        res = self.url_open(wrong_token_url)
        self.assertEqual(res.status_code, 200, "Shouldn't raise any error")
        self.assertNotEqual(res.url, order_url, "Should've been redirected")
        # Case 2: Attempt to access with an unexistant sale order
        wrong_order_url = re.sub(r"(?<=res_id=)([0-9]+)", str(order.id + 1), order_url,)
        res = self.url_open(wrong_order_url)
        self.assertEqual(res.status_code, 200, "Shouldn't raise any error")
        self.assertNotEqual(res.url, order_url, "Should've been redirected")

    def test_04_download_badge_another_order(self):
        # Create sale orders
        order1 = self.env["sale.order"].create(
            {
                "partner_id": self.customer.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.product_event.id,
                            "name": "Event registration",
                            "event_id": self.event.id,
                            "event_ticket_id": self.ticket_adults.id,
                            "price_unit": 15.00,
                            "product_uom_qty": 1,
                        },
                    ),
                ],
            }
        )
        order2 = self.env["sale.order"].create(
            {
                "partner_id": self.customer.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.product_event.id,
                            "name": "Event registration",
                            "event_id": self.event.id,
                            "event_ticket_id": self.ticket_adults.id,
                            "price_unit": 15.00,
                            "product_uom_qty": 1,
                        },
                    ),
                ],
            }
        )
        # Confirm order and registrations
        order1.action_confirm()
        order2.action_confirm()
        order1.order_line._update_registrations(confirm=True)
        order2.order_line._update_registrations(confirm=True)
        # Get portal url
        badge_url = "/my/orders/%d/event/%d/badge/%d?access_token=%s"
        order_url = order1._get_share_url()
        access_token = re.search(r"(?<=access_token=)([^&]+)", order_url).group(0)
        # Attempt to download a badge from this order
        res = self.url_open(
            badge_url
            % (
                order1.id,
                self.event.id,
                order1.event_registration_ids[0].id,
                access_token,
            )
        )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers["Content-Type"], "application/pdf")
        # Attempt to download a badge from another order
        res = self.url_open(
            badge_url
            % (
                order1.id,
                self.event.id,
                order2.event_registration_ids[0].id,
                access_token,
            )
        )
        self.assertEqual(res.status_code, 200)
        self.assertNotEqual(res.headers["Content-Type"], "application/pdf")
