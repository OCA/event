# Copyright 2024 Camptocamp (http://www.camptocamp.com).
# @author Italo LOPES <i.lopes@nomadiplus.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpCase, tagged


@tagged("post_install", "-at_install")
class TestWebsiteEventSaleSeatReserve(HttpCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        test_context = cls.env.context.copy()
        test_context["test_event_seat_reserve"] = True
        cls.env = cls.env(context=dict(test_context, tracking_disable=True))
        # Event
        cls.event = cls.env.ref("event.event_4")
        cls.event_ticket = cls.env.ref("event.event_4_ticket_0")
        cls.event_product = cls.env.ref("event_sale.product_product_event")
        # Websites
        cls.website_1 = cls.env.ref("website.default_website")
        # Orders
        cls.partner = cls.env.ref("base.res_partner_1")
        cls.partner2 = cls.env.ref("base.res_partner_2")
        cls.order_1 = cls.env["sale.order"].create(
            {
                "partner_id": cls.partner.id,
                "team_id": cls.env.ref("sales_team.salesteam_website_sales").id,
                "payment_term_id": cls.env.ref(
                    "account.account_payment_term_end_following_month"
                ).id,
            }
        )

        cls.env["sale.order.line"].create(
            {
                "product_id": cls.event_product.id,
                "price_unit": 30,
                "order_id": cls.order_1.id,
                "event_id": cls.event.id,
                "event_ticket_id": cls.event_ticket.id,
            }
        )

    def test_add_event_to_cart(self):
        existing_orders = self.env["sale.order"].search([])
        # In frontend, create an order
        self.start_tour(
            "/event", "tour_website_event_sale_seat_reserve", login="portal"
        )
        created_order = self.env["sale.order"].search(
            [("id", "not in", existing_orders.ids)]
        )
        self.assertEqual(created_order.state, "draft")
        created_registration = self.env["event.registration"].search(
            [("sale_order_id", "=", created_order.id)]
        )
        self.assertEqual(len(created_registration), 1)
        self.assertEqual(created_registration.event_id, self.event)
        self.assertEqual(created_registration.state, "reserved")
