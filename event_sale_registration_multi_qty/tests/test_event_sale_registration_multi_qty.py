# Copyright 2017-19 Tecnativa - David Vidal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0).
from odoo.tests import common


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
                "seats_availability": "limited",
                "seats_max": "100",
                "seats_min": "1",
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
                "seats_availability": "limited",
                "seats_max": "100",
                "seats_min": "1",
                "event_ticket_ids": [
                    (0, 0, {"product_id": cls.product.id, "name": "test1"}),
                ],
                "registration_multi_qty": False,
            }
        )
        cls.partner = cls.env["res.partner"].create({"name": "Test partner"})
        cls.so_line_e_multi = (
            0,
            0,
            {
                "product_id": cls.product.id,
                "event_id": cls.event_multi.id,
                "product_uom_qty": 5.0,
                "event_ticket_id": cls.event_multi.event_ticket_ids[0].id,
            },
        )
        cls.so_line_e_nomulti = (
            0,
            0,
            {
                "product_id": cls.product.id,
                "event_id": cls.event_nomulti.id,
                "product_uom_qty": 5.0,
                "event_ticket_id": cls.event_nomulti.event_ticket_ids[0].id,
            },
        )

    def test_sale_multi(self):
        sale = self.env["sale.order"].create(
            {"partner_id": self.partner.id, "order_line": [self.so_line_e_multi]}
        )
        sale.action_confirm()
        reg = self.env["event.registration"].search([("sale_order_id", "=", sale.id)])
        self.assertEqual(len(reg), 1)
        self.assertEqual(reg.qty, 5)
        self.assertEqual(reg.event_id, self.event_multi)
        self.assertEqual(reg.state, "draft")

    def test_sale_registration_editor(self):
        sale = self.env["sale.order"].create(
            {"partner_id": self.partner.id, "order_line": [self.so_line_e_multi]}
        )
        editor = self.env["registration.editor"].create(
            {
                "sale_order_id": sale.id,
                "event_registration_ids": [
                    (
                        0,
                        0,
                        {"event_id": self.so_line_e_multi[2]["event_id"], "qty": 10},
                    )
                ],
            }
        )
        editor.action_make_registration()
        reg = self.env["event.registration"].search([("sale_order_id", "=", sale.id)])
        self.assertEqual(reg.qty, 10)

    def test_sale_nomulti(self):
        sale = self.env["sale.order"].create(
            {"partner_id": self.partner.id, "order_line": [self.so_line_e_nomulti]}
        )
        sale.action_confirm()
        regs = self.env["event.registration"].search([("sale_order_id", "=", sale.id)])
        self.assertEqual(len(regs), 5)
        for reg in regs:
            self.assertEqual(reg.qty, 1)
            self.assertEqual(reg.event_id, self.event_nomulti)
            self.assertEqual(reg.state, "draft")

    def test_sale_mixed(self):
        sale = self.env["sale.order"].create(
            {
                "partner_id": self.partner.id,
                "order_line": [self.so_line_e_nomulti, self.so_line_e_multi],
            }
        )
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
