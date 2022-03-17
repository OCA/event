# Copyright 2017-19 Tecnativa - David Vidal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0).
from odoo.exceptions import ValidationError
from odoo.tests import Form, common


class EventSaleSession(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product_category = cls.env["product.category"].create({"name": "test_cat"})
        cls.product = cls.env["product.product"].create(
            {
                "name": "Test product event",
                "type": "service",
                "event_ok": True,
                "lst_price": 10.0,
                "categ_id": cls.product_category.id,
            }
        )
        cls.event = cls.env["event.event"].create(
            {
                "name": "Test event",
                "date_begin": "2017-05-26 20:00:00",
                "date_end": "2017-05-30 22:00:00",
                "seats_limited": True,
                "seats_max": "100",
                "event_ticket_ids": [
                    (0, 0, {"product_id": cls.product.id, "name": "test1"}),
                    (
                        0,
                        0,
                        {"product_id": cls.product.id, "name": "test2", "price": 8.0},
                    ),
                ],
            }
        )
        cls.event2 = cls.env["event.event"].create(
            {
                "name": "Test event",
                "date_begin": "2017-05-26 20:00:00",
                "date_end": "2017-05-30 22:00:00",
                "seats_limited": True,
                "seats_max": "50",
                "event_ticket_ids": [
                    (0, 0, {"product_id": cls.product.id, "name": "test1"}),
                ],
            }
        )
        cls.session = cls.env["event.session"].create(
            {
                "name": "Test session",
                "date_begin": "2017-05-26 20:00:00",
                "date_end": "2017-05-26 22:00:00",
                "event_id": cls.event.id,
            }
        )
        cls.session_alt_1 = cls.env["event.session"].create(
            {
                "name": "Test Alternative Session",
                "date_begin": "2017-05-27 20:00:00",
                "date_end": "2017-05-27 22:00:00",
                "event_id": cls.event.id,
            }
        )
        cls.session_alt_2 = cls.env["event.session"].create(
            {
                "name": "Test Alternative Session",
                "date_begin": "2017-05-27 20:00:00",
                "date_end": "2017-05-27 22:00:00",
                "event_id": cls.event2.id,
            }
        )
        cls.partner = cls.env["res.partner"].create({"name": "Test partner"})

    def test_sale(self):
        """Sell an event with session"""
        sale_form = Form(self.env["sale.order"])
        sale_form.partner_id = self.partner
        with sale_form.order_line.new() as line:
            line.product_id = self.product
            line.event_id = self.event
            line.session_id = self.session
            line.event_ticket_id = self.event.event_ticket_ids[:1]
            line.product_uom_qty = 5
        sale = sale_form.save()
        self.assertEqual(self.session.unconfirmed_qty, 5)
        self.assertEqual(self.event.unconfirmed_qty, 5)
        sale.action_confirm()
        self.assertEqual(self.session.unconfirmed_qty, 0)
        self.assertEqual(self.event.unconfirmed_qty, 0)
        regs = self.env["event.registration"].search([("sale_order_id", "=", sale.id)])
        self.assertEqual(len(regs), 5)
        for reg in regs:
            self.assertEqual(reg.event_id, self.event)
            self.assertEqual(reg.session_id, self.session)
            self.assertEqual(reg.partner_id, self.partner)
            self.assertEqual(reg.name, self.partner.name)

    def test_session_overbooking(self):
        """Sell an event with session"""
        sale_form = Form(self.env["sale.order"])
        sale_form.partner_id = self.partner
        with sale_form.order_line.new() as line:
            line.product_id = self.product
            line.event_id = self.event
            line.session_id = self.session
            line.event_ticket_id = self.event.event_ticket_ids[:1]
            line.product_uom_qty = 60
        sale = sale_form.save()
        self.assertTrue(sale._session_seats_available())
        sale_form = Form(sale)
        with sale_form.order_line.new() as line:
            line.product_id = self.product
            line.event_id = self.event
            line.session_id = self.session
            line.event_ticket_id = self.event.event_ticket_ids[:1]
            line.product_uom_qty = 40
        sale_form.save()
        # We can order up to the limit of 100 for this session
        self.assertTrue(sale._session_seats_available())
        # If we try to book another seat, an error will raise
        with self.assertRaises(ValidationError):
            sale.order_line[1].product_uom_qty += 1
            sale.order_line[1].product_uom_change()
        # It's not allowed to overbook in a session with not enough seats
        self.session_alt_1.seats_max = 50
        with self.assertRaises(ValidationError):
            sale.order_line[0].session_id = self.session_alt_1
            sale.order_line[0].onchange_session_id()
