# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# © 2015 Grupo ESOC Ingeniería de Servicios, S.L.U. - Jairo Llopis

from .base import BaseCase
from .. import exceptions as ex


class ProductsCase(BaseCase):
    def setUp(self):
        super(ProductsCase, self).setUp()
        # Add good duration types
        self.course.product_ids |= self.products

    def test_copy_course(self):
        """Copy course with products."""
        new = self.course.copy()
        self.assertEqual(new.product_ids, self.course.product_ids)

    def test_fill_products(self):
        """Changing course changes products."""
        self.event.course_id = self.course
        self.event._fill_product_ids()
        self.assertEqual(self.event.product_ids, self.course.product_ids)

    def test_event_has_products_not_fill_products(self):
        """No products changed because event already had one."""
        self.event.product_ids = self.product_1
        self.event.course_id = self.course
        self.event._fill_product_ids()
        self.assertEqual(self.event.product_ids, self.product_1)

    def test_delivered_products(self):
        """Products get delivered."""
        self.event.course_id = self.course
        self.event.product_ids = self.products
        self.event._onchange_product_ids_check_delivered()
        self.event.registration_ids = self.create(
            "event.registration",
            {"name": u"Registrätion",
             "event_id": self.event.id,
             "products_delivered": True})
        self.assertTrue(self.event.registration_ids.products_delivered)

    def test_block_deliver_no_products(self):
        """Cannot deliver products if they are not set in the event."""
        with self.assertRaises(ex.NoProductsToDeliverError):
            self.event.registration_ids = self.create(
                "event.registration",
                {"name": u"Registrätion",
                 "event_id": self.event.id,
                 "products_delivered": True})

    def test_block_remove_delivered_products(self):
        """Cannot change products if they have been delivered."""
        self.event.course_id = self.course
        self.event.product_ids = self.products
        self.event._onchange_product_ids_check_delivered()
        self.event.registration_ids = self.create(
            "event.registration",
            {"name": u"Registrätion",
             "event_id": self.event.id,
             "products_delivered": True})
        with self.assertRaises(ex.ChangeDeliveredProductsWarning):
            self.event.product_ids -= self.product_1
            self.event._onchange_product_ids_check_delivered()
