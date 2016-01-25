# -*- coding: utf-8 -*-
# © 2015 Grupo ESOC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import datetime, timedelta
from openerp.tests.common import TransactionCase


class BaseCase(TransactionCase):
    """Base test case class."""
    def setUp(self):
        """Create needed records."""
        super(BaseCase, self).setUp()
        self.event_type = self.env["event.type"].create({
            "name": "Test event tỳpe",
        })
        self.event = self.env["event.event"].create({
            "name": u"Test ëvent",
            "type": self.event_type.id,
            "date_begin": datetime.now(),
            "date_end": datetime.now() + timedelta(weeks=1),
        })
        self.partner_0 = self.env["res.partner"].create({
            "name": u"Têst company partner 0",
            "is_company": True,
        })
        self.partner_1 = self.env["res.partner"].create({
            "name": u"Têst person partner 1",
            "is_company": False,
            "parent_id": self.partner_0.id,
        })
        self.partner_2 = self.env["res.partner"].create({
            "name": u"Têst person partner 2",
            "is_company": False,
            "parent_id": self.partner_0.id,
        })
        self.sale_order = self.env["sale.order"].create({
            "partner_id": self.partner_1.id,
        })
        self.product_tmpl = self.env["product.template"].create({
            "name": u"Tëst product template",
            "type": "service",
            "sale_ok": True,
            "event_ok": True,
            "event_type_id": self.event_type.id,
            "list_price": 100.1,
        })
        self.product = self.env["product.product"].create({
            "product_tmpl_id": self.product_tmpl.id,
            "lst_price": 200.2,
        })
        self.ticket = self.env["event.event.ticket"].create({
            "name": u"Test tícket",
            "event_id": self.event.id,
            "price": 300.3,
        })

    def create_generator(self):
        """Get a new generator wizard."""
        return self.env["event_sale_pro.quotation_generator"].create({
            "event_id": self.event.id,
            "product_id": self.product.id,
        })

    def create_line(self, data=None):
        """Create a sale order line."""
        data = data or dict()

        # New line in sale order
        data.setdefault("event_id", self.event.id)
        data.setdefault("event_ticket_id", self.ticket.id)
        data.setdefault("order_id", self.sale_order.id)
        data.setdefault("product_id", self.product.id)
        line = self.env["sale.order.line"].create(data)

        # Load ticket price
        line.update(
            line.onchange_event_ticket_id(
                event_ticket_id=line.event_ticket_id.id)["value"])

        return line

    def create_registrations(self):
        """Create some registrations in the event."""
        self.registration_1 = self.env["event.registration"].create({
            "event_id": self.event.id,
            "partner_id": self.partner_1.id,
            "nb_register": 1,
        })
        self.registration_2 = self.env["event.registration"].create({
            "event_id": self.event.id,
            "partner_id": self.partner_2.id,
            "nb_register": 2,
        })
        return self.registration_1 | self.registration_2
