# Copyright 2025 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from dateutil.relativedelta import relativedelta

from odoo import Command, fields
from odoo.tests import TransactionCase


class TestEventSaleFreeNoInvoiceable(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        now = fields.Datetime.now()
        cls.event = cls.env["event.event"].create(
            {
                "name": "Test event no invoiceable",
                "date_begin": now + relativedelta(days=1),
                "date_end": now + relativedelta(days=3),
                "event_type_id": cls.env.ref("event.event_type_1").id,
                "event_ticket_ids": [
                    Command.create({"name": "Ticket One", "price": 0})
                ],
            }
        )
        cls.partner = cls.env["res.partner"].create({"name": "Partner nso invoiceable"})
        cls.ticket = cls.event.event_ticket_ids[0]
        cls.order = cls.env["sale.order"].create(
            {
                "partner_id": cls.partner.id,
                "order_line": [
                    Command.create(
                        {
                            "product_id": cls.ticket.product_id.id,
                            "event_id": cls.event.id,
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
        self.order.order_line = [
            Command.create(
                {
                    "product_id": self.ticket.product_id.id,
                    "event_id": self.event.id,
                    "event_ticket_id": self.ticket.id,
                    "price_unit": 10,
                }
            )
        ]
        self.order.action_confirm()
        self.assertEqual(self.order.invoice_status, "to invoice")
        self.assertEqual(self.order.order_line[0].invoice_status, "no")
        self.assertEqual(self.order.order_line[1].invoice_status, "to invoice")
