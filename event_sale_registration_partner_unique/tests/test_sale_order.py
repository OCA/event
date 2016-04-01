# -*- coding: utf-8 -*-
# © 2016 Antiun Ingeniería S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class SomethingCase(TransactionCase):
    def setUp(self, *args, **kwargs):
        super(SomethingCase, self).setUp(*args, **kwargs)
        self.partner = self.env.ref("base.res_partner_2")
        self.event = self.env.ref("event.event_3")
        self.event.forbid_duplicates = True
        self.sale_order = self.env["sale.order"].create({
            "partner_id": self.partner.id,
        })
        self.sale_order.order_line |= self.env["sale.order.line"].create({
            "order_id": self.sale_order.id,
            "product_id": self.env.ref("event_sale.event_3_product").id,
            "event_id": self.event.id,
            "event_ticket_id": self.env.ref("event_sale.event_3_ticket_1").id,
            "product_uom_qty": 1,
            "price_unit": 1000,
        })

    def test_nodupe(self):
        """Everything works as before without duplicates."""
        self.sale_order.action_button_confirm()
        self.assertEqual(self.event.registration_ids.partner_id, self.partner)
        self.assertEqual(self.event.registration_ids.nb_register, 1)

    def test_dupe(self):
        """Everything works when duplicates are found."""
        self.sale_order.action_button_confirm()
        newso = self.sale_order.copy()
        newso.action_button_confirm()
        self.assertEqual(self.event.registration_ids.partner_id, self.partner)
        self.assertEqual(self.event.registration_ids.nb_register, 2)

    def test_dupe_different_ticket(self):
        """Duplicates allowed when ticket type differs."""
        self.sale_order.action_button_confirm()
        newso1 = self.sale_order.copy()
        newso1.order_line.event_ticket_id = False
        newso1.action_button_confirm()
        newso2 = newso1.copy()
        newso2.action_button_confirm()
        for r in self.event.registration_ids:
            if r.event_ticket_id:
                self.assertEqual(r.nb_register, 1)
            else:
                self.assertEqual(r.nb_register, 2)
