# Copyright 2024 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestEventSaleSeatReserve(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # ../event/data/event_demo.xml
        # using this demo data, we have a max_seats = 4
        # and 3 registrations
        cls.event = cls.env.ref("event.event_4")
        cls.event_ticket = cls.env.ref("event.event_4_ticket_0")
        cls.event_product = cls.env.ref("event_sale.product_product_event")
        cls.partner = cls.env.ref("base.res_partner_1")
        cls.partner2 = cls.env.ref("base.res_partner_2")
        cls.sale_order1 = cls.env["sale.order"].create(
            {
                "partner_id": cls.partner.id,
                "payment_term_id": cls.env.ref(
                    "account.account_payment_term_end_following_month"
                ).id,
            }
        )

        cls.env["sale.order.line"].create(
            {
                "product_id": cls.event_product.id,
                "price_unit": 30,
                "order_id": cls.sale_order1.id,
                "event_id": cls.event.id,
                "event_ticket_id": cls.event_ticket.id,
            }
        )

        cls.registration1 = cls.env["event.registration"].create(
            {
                "event_id": cls.event.id,
                "event_ticket_id": cls.event_ticket.id,
                "name": cls.partner.name,
                "partner_id": cls.partner.id,
                "sale_order_id": cls.sale_order1.id,
                "sale_order_line_id": cls.sale_order1.order_line.id,
            }
        )

        cls.sale_order2 = cls.env["sale.order"].create(
            {
                "partner_id": cls.partner2.id,
                "payment_term_id": cls.env.ref(
                    "account.account_payment_term_end_following_month"
                ).id,
            }
        )

        cls.env["sale.order.line"].create(
            {
                "product_id": cls.event_product.id,
                "price_unit": 30,
                "order_id": cls.sale_order2.id,
                "event_id": cls.event.id,
                "event_ticket_id": cls.event_ticket.id,
            }
        )

        cls.registration2 = cls.env["event.registration"].create(
            {
                "event_id": cls.event.id,
                "event_ticket_id": cls.event_ticket.id,
                "name": cls.partner2.name,
                "partner_id": cls.partner2.id,
                "sale_order_id": cls.sale_order2.id,
                "sale_order_line_id": cls.sale_order2.order_line.id,
            }
        )

    def test_01_confirm_sale(self):
        """
        Test that reserved quantity is set and if seats are available or not
        """
        self.sale_order1.action_confirm()
        self.assertEqual(self.event_ticket.seats_reserved_unconfirmed, 1)
        self.assertEqual(self.registration1.state, "reserved")
        self.assertEqual(self.event.seats_available, 0)

    def test_02_confirm_sale_no_available_seats(self):
        """
        Test that reserved quantity is set and if seats are available or not
        """
        self.sale_order1.action_confirm()
        with self.assertRaisesRegex(
            ValidationError, "There are not enough seats available*"
        ):
            self.sale_order2.action_confirm()

    def test_03_reset_confirmed_sale_to_draft(self):
        """
        Test if the reserved quantity is set to 0 when the sale is reset to draft
        """
        self.sale_order1.action_confirm()
        self.assertEqual(self.event_ticket.seats_reserved_unconfirmed, 1)
        self.assertEqual(self.registration1.state, "reserved")
        self.assertEqual(self.event.seats_available, 0)
        self.sale_order1.action_draft()
        self.assertEqual(self.event_ticket.seats_reserved_unconfirmed, 0)
        self.assertEqual(self.registration1.state, "draft")
        self.assertEqual(self.event.seats_available, 1)
