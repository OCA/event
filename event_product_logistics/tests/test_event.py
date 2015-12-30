# -*- coding: utf-8 -*-
# © 2015 Grupo ESOC Ingeniería de Servicios, S.L.U. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase
from .base import BaseCase
from openerp import exceptions


class EventEventCase(BaseCase, TransactionCase):
    def test_loading_deliverable_products(self):
        """Load deliverable products."""
        self.product.event_deliverable_product_ids = self.deliverable_products
        self.event.product_id = self.product
        self.event.action_load_deliverable_products()
        self.assertEqual(
            self.event.deliverable_product_ids,
            self.deliverable_products)

    def test_products_delivered_to_all(self):
        """Marks products as delivered to all attendees."""
        self.event.deliverable_product_ids = self.deliverable_products
        for n in range(4):
            self.event_registration.copy()
        self.event.action_products_delivered_to_all()
        self.assertEqual(
            self.event.mapped("registration_ids.products_delivered"),
            [True] * 5)

    def test_changing_delivered_products(self):
        """Odoo warns you if you change already delivered products."""
        self.event.deliverable_product_ids = self.deliverable_products
        self.event.registration_ids.write({"products_delivered": True})
        with self.env.do_in_onchange():
            self.event.deliverable_product_ids = self.deliverable_products[0]
            with self.assertRaises(exceptions.Warning):
                self.event._onchange_deliverable_product_ids()


class EventRegistrationCase(BaseCase, TransactionCase):
    def test_can_deliver_products(self):
        """Able to deliver products to registrations."""
        self.event.deliverable_product_ids = self.deliverable_products
        self.event_registration.products_delivered = True

    def test_cannot_deliver_products(self):
        """Unable to deliver products to registrations."""
        with self.assertRaises(exceptions.ValidationError):
            self.event_registration.products_delivered = True
