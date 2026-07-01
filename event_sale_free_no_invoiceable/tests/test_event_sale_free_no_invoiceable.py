# Copyright 2025 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import Command

from odoo.addons.event_sale.tests.common import TestEventSaleCommon


class TestEventSaleFreeNoInvoiceable(TestEventSaleCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.event_0.write(
            {
                "event_ticket_ids": [
                    Command.create({"name": "Ticket One", "price": 0})
                ],
            }
        )
        cls.partner = cls.env["res.partner"].create({"name": "Partner nso invoiceable"})
        cls.ticket = cls.event_0.event_ticket_ids[0]
        cls.order = cls.env["sale.order"].create(
            {
                "partner_id": cls.partner.id,
                "order_line": [
                    Command.create(
                        {
                            "product_id": cls.ticket.product_id.id,
                            "event_id": cls.event_0.id,
                            "event_ticket_id": cls.ticket.id,
                        }
                    ),
                ],
            }
        )

    def test_no_invoiceable(self):
        self.order.action_confirm()
        self.assertEqual(self.order.invoice_status, "no")

    def test_invoiceable(self):
        self.order.order_line.price_unit = 10
        self.order.action_confirm()
        self.assertEqual(self.order.invoice_status, "to invoice")

    def test_mix(self):
        line_0 = self.order.order_line
        self.order.order_line = [
            Command.create(
                {
                    "product_id": self.ticket.product_id.id,
                    "event_id": self.event_0.id,
                    "event_ticket_id": self.ticket.id,
                    "price_unit": 10,
                }
            )
        ]
        line_extra = self.order.order_line - line_0
        self.order.action_confirm()
        self.assertEqual(self.order.invoice_status, "to invoice")
        self.assertEqual(line_0.invoice_status, "no")
        self.assertEqual(line_extra.invoice_status, "to invoice")
