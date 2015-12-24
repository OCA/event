# -*- coding: utf-8 -*-
# © 2015 Grupo ESOC Ingeniería de Servicios, S.L.U. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase
from .base import BaseCase
from .. import exceptions as ex


class ProductTemplateCase(BaseCase, TransactionCase):
    model = "product.template"

    def setUp(self, *args, **kwargs):
        result = super(ProductTemplateCase, self).setUp(*args, **kwargs)

        self.product_new = self.env[self.model].new({
            "name": u"Test pròduct 1",
        })

        return result

    def _assign_type_and_event(self):
        """Assign type to event and product, and link them."""
        self.product.event_type_id = self.event_type_1
        self.event.type = self.event_type_1
        self.event.product_id = self.product

    def prod(self):
        """Choose created ``product.template``."""
        return self.product.product_tmpl_id

    def test_is_event_disables_event_ok(self):
        """Setting ``is_event`` disables ``event_ok``."""
        self.product_new.event_ok = True
        self.product_new.update(
            self.product_new.onchange_event_ok(
                self.product_new.event_type_id,
                self.product_new.event_ok).get("value", dict()))
        self.product_new.is_event = True
        self.product_new._onchange_is_event()

        self.assertTrue(self.product_new.is_event)
        self.assertFalse(self.product_new.event_ok)
        self.assertEqual(self.product_new.type, "service")

    def test_event_ok_disables_is_event(self):
        """Setting ``event_ok`` disables ``is_event``."""
        self.product_new.is_event = True
        self.product_new._onchange_is_event()
        self.product_new.event_ok = True
        self.product_new.update(
            self.product_new.onchange_event_ok(
                self.product_new.event_type_id,
                self.product_new.event_ok).get("value", dict()))

        self.assertFalse(self.product_new.is_event)
        self.assertTrue(self.product_new.event_ok)
        self.assertEqual(self.product_new.type, "service")

    def test_is_event_and_event_ok_forbidden(self):
        """Cannot write if ``is_event`` and ``event_ok`` are ``True``."""
        with self.assertRaises(ex.EventAndTicketError):
            self.prod().write({
                "is_event": True,
                "event_ok": True,
            })

    def test_change_used_event_product(self):
        """Block changing a used event product."""
        self.prod().is_event = True
        self.event.product_id = self.product
        with self.assertRaises(ex.ProductIsNotEventError):
            self.prod().is_event = False

    def test_change_event_type(self):
        """Block changing event type in case of conflict."""
        self.prod().is_event = True
        self._assign_type_and_event()
        with self.assertRaises(ex.TypeMismatchError):
            self.prod().event_type_id = self.event_type_2

    def test_remove_event_type(self):
        """Block changing event type in case of conflict."""
        self.prod().is_event = True
        self._assign_type_and_event()
        self.prod().event_type_id = False

    def test_link_normal_product_to_event(self):
        """Block linking normal product to an event."""
        with self.assertRaises(ex.ProductIsNotEventError):
            self.product.event_ids |= self.event


class ProductProductCase(ProductTemplateCase):
    model = "product.product"

    def prod(self):
        """Choose created ``product.product``."""
        return self.product

    def test_event_count(self):
        """Event count is right in template and product."""
        # We have 2 event products
        self.product.is_event = True
        products = [self.product, self.product.copy()]
        templates = [p.product_tmpl_id for p in products]

        # Both are variants of the same template
        products[1].product_tmpl_id = products[0].product_tmpl_id

        # We have 5 events
        events = [self.event.copy() for n in range(5)]

        # 3 events for first product, 2 for the second
        counts = [3, 2]
        for event in events[:3]:
            event.product_id = products[0]
        for event in events[3:]:
            event.product_id = products[1]

        # Check event count per product
        for n in range(2):
            self.assertEqual(products[n].event_count, counts[n])

        # Check event count per template
        self.assertEqual(templates[0].event_count, 5)
        self.assertEqual(templates[1].event_count, 0)
