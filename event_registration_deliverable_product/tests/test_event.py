# -*- coding: utf-8 -*-
# © 2015 Grupo ESOC Ingeniería de Servicios, S.L.U. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase
from .base import BaseCase
from .. import exceptions


class EventEventCase(BaseCase, TransactionCase):
    def test_loading_deliverable_products(self):
        """Load deliverable products."""
        self.product.event_deliverable_product_ids = self.deliverable_products
        self.event.product_id = self.product
        self.event.action_load_deliverable_products()
        self.assertEqual(
            self.event.deliverable_product_ids,
            self.deliverable_products)


class EventRegistrationCase(BaseCase, TransactionCase):
    def test_can_deliver_products(self):
        """Able to deliver products to registrations."""
        self.event.deliverable_product_ids = self.deliverable_products
        self.event_registration.products_delivered = True

    def test_cannot_deliver_products(self):
        """Unable to deliver products to registrations."""
        with self.assertRaises(exceptions.NoProductsToDeliverError):
            self.event_registration.products_delivered = True
