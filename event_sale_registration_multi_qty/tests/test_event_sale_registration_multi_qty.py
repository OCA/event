# Copyright 2017-19 Tecnativa - David Vidal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0).
from odoo.tests import Form, common


class TestEventSaleRegistrationMultiQty(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestEventSaleRegistrationMultiQty, cls).setUpClass()
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
        cls.event_multi = cls.env["event.event"].create(
            {
                "name": "Test event multi",
                "date_begin": "2017-05-26 20:00:00",
                "date_end": "2017-05-30 22:00:00",
                "seats_limited": True,
                "seats_max": "100",
                "event_ticket_ids": [
                    (0, 0, {"product_id": cls.product.id, "name": "test1"}),
                ],
                "registration_multi_qty": True,
            }
        )
        cls.event_nomulti = cls.env["event.event"].create(
            {
                "name": "Test event no multi",
                "date_begin": "2017-05-26 20:00:00",
                "date_end": "2017-05-30 22:00:00",
                "seats_limited": True,
                "seats_max": "100",
                "event_ticket_ids": [
                    (0, 0, {"product_id": cls.product.id, "name": "test1"}),
                ],
                "registration_multi_qty": False,
            }
        )
        cls.partner = cls.env["res.partner"].create({"name": "Test partner"})

    def _add_so_line_event(self, sale, event, qty=5):
        """Helper method to quickly add sale lines"""
        sale_form = Form(sale)
        with sale_form.order_line.new() as line:
            line.product_id = self.product
            line.event_id = event
            line.product_uom_qty = qty
            line.event_ticket_id = event.event_ticket_ids[:1]
        sale_form.save()

    def _create_sale(self):
        sale_form = Form(self.env["sale.order"])
        sale_form.partner_id = self.partner
        return sale_form

    def test_sale_multi(self):
        sale = self._create_sale().save()
        self._add_so_line_event(sale, self.event_multi)
        sale.action_confirm()
        reg = self.env["event.registration"].search([("sale_order_id", "=", sale.id)])
        self.assertEqual(len(reg), 1)
        self.assertEqual(reg.qty, 5)
        self.assertEqual(reg.event_id, self.event_multi)
        self.assertEqual(reg.state, "draft")

    def test_sale_nomulti(self):
        sale = self._create_sale().save()
        self._add_so_line_event(sale, self.event_nomulti)
        sale.action_confirm()
        regs = self.env["event.registration"].search([("sale_order_id", "=", sale.id)])
        self.assertEqual(len(regs), 5)
        for reg in regs:
            self.assertEqual(reg.qty, 1)
            self.assertEqual(reg.event_id, self.event_nomulti)
            self.assertEqual(reg.state, "draft")

    def test_sale_mixed(self):
        sale = self._create_sale().save()
        self._add_so_line_event(sale, self.event_multi)
        self._add_so_line_event(sale, self.event_nomulti)
        sale.action_confirm()
        regs = self.env["event.registration"].search([("sale_order_id", "=", sale.id)])
        self.assertEqual(len(regs), 6)
        for reg in regs:
            self.assertEqual(reg.state, "draft")
            if reg.event_id == self.event_multi:
                self.assertEqual(reg.qty, 5)
            else:
                self.assertEqual(reg.event_id, self.event_nomulti)
                self.assertEqual(reg.qty, 1)
