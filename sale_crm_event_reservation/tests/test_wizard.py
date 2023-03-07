# Copyright 2021 Tecnativa - Jairo Llopis
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from datetime import datetime, timedelta

from odoo.tests.common import Form, TransactionCase


class OpportunityCase(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.pricelist = cls.env["product.pricelist"].create(
            {
                "name": "Test pricelist",
                "currency_id": cls.env.company.currency_id.id,
                "item_ids": [
                    (
                        0,
                        0,
                        {
                            "applied_on": "3_global",
                            "compute_price": "formula",
                            "base": "list_price",
                        },
                    )
                ],
            }
        )
        cls.partner_1 = cls.env["res.partner"].create(
            [{"name": "Fulanito", "property_product_pricelist": cls.pricelist.id}]
        )
        cls.event_type_1 = cls.env["event.type"].create({"name": "Ev. Type 1"})
        cls.product_reservation_1 = cls.env["product.product"].create(
            {
                "sale_ok": True,
                "detailed_type": "event_reservation",
                "event_reservation_type_id": cls.event_type_1.id,
                "lst_price": 11,
                "name": "reservation for ev. type 1",
            }
        )
        cls.product_ticket_1 = cls.env["product.product"].create(
            {"name": "events ticket", "detailed_type": "event", "lst_price": 10}
        )
        cls.event_1 = cls.env["event.event"].create(
            {
                "name": "Ev. 1",
                "date_begin": datetime.now() + timedelta(days=1),
                "date_end": datetime.now() + timedelta(days=2),
                "event_ticket_ids": [
                    (
                        0,
                        0,
                        {
                            "name": "ticket 1",
                            "product_id": cls.product_ticket_1.id,
                            "price": 2,  # Differs from product price
                        },
                    )
                ],
            }
        )
        cls.opportunity_1 = cls.env["crm.lead"].create(
            {
                "partner_id": cls.partner_1.id,
                "name": "I'm selling an event!",
                "event_type_id": cls.event_type_1.id,
                "seats_wanted": 3,
            }
        )

    def test_register(self):
        """Generate event registration quotation."""
        wiz_form = Form(
            self.env["crm.lead.event.sale.wizard"].with_context(
                default_opportunity_id=self.opportunity_1.id
            )
        )
        wiz_form.mode = "register"
        wiz_form.event_id = self.event_1
        wiz_form.event_ticket_id = self.event_1.event_ticket_ids[0]
        action = wiz_form.save().action_generate()
        self.assertEqual(action["res_model"], "sale.order")
        so = self.env["sale.order"].browse(action["res_id"])
        self.assertEqual(so.order_line.product_id, self.product_ticket_1)
        self.assertEqual(so.order_line.event_id, self.event_1)
        self.assertEqual(
            so.order_line.event_ticket_id, self.event_1.event_ticket_ids[0]
        )
        self.assertTrue(so.order_line.event_ok)
        self.assertEqual(
            so.order_line.product_uom_qty,
            3,
            "SO line qty = opportunity.seats_wanted",
        )
        self.assertAlmostEqual(
            so.amount_untaxed,
            6,
            msg="Amount = opportunity.seats_wanted * ticket.price",
        )
        self.assertEqual(so.state, "draft")

    def test_reserve(self):
        """Generate event reservation quotation."""
        wiz_form = Form(
            self.env["crm.lead.event.sale.wizard"].with_context(
                default_opportunity_id=self.opportunity_1.id
            )
        )
        wiz_form.mode = "reserve"
        wiz_form.product_id = self.product_reservation_1
        action = wiz_form.save().action_generate()
        self.assertEqual(action["res_model"], "sale.order")
        so = self.env["sale.order"].browse(action["res_id"])
        self.assertEqual(so.order_line.product_id, self.product_reservation_1)
        self.assertFalse(so.order_line.event_id)
        self.assertFalse(so.order_line.event_ticket_id)
        self.assertFalse(so.order_line.event_ok)
        self.assertEqual(
            so.order_line.product_uom_qty,
            3,
            "SO line qty = opportunity.seats_wanted",
        )
        self.assertAlmostEqual(
            so.amount_untaxed,
            33,
            msg="Amount = opportunity.seats_wanted * reservation.price",
        )
        self.assertEqual(so.state, "draft")
