# -*- coding: utf-8 -*-
# © 2015 Grupo ESOC Ingeniería de Servicios, S.L.U. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase
from .base import BaseCase
from .. import exceptions as ex


class EventEventCase(BaseCase, TransactionCase):
    def setUp(self, *args, **kwargs):
        result = super(EventEventCase, self).setUp(*args, **kwargs)
        self.product.is_event = True
        self.event_new = self.env["event.event"].new({
            "name": "Event 2",
            "date_begin": "2015-11-26",
            "date_end": "2015-11-30",
        })
        return result

    def test_link_wrong_product(self):
        """Cannot link a non-event product."""
        self.product.is_event = False
        with self.assertRaises(ex.ProductIsNotEventError):
            self.event.product_id = self.product

    def test_link_event_no_type(self):
        """Cannot link to typed product if event has no type."""
        self.product.event_type_id = self.event_type_1
        with self.assertRaises(ex.TypeMismatchError):
            self.event.product_id = self.product

    def test_link_product_no_type(self):
        """Allow to link to a product with no type."""
        self.event.type = self.event_type_1
        self.event.product_id = self.product

    def test_link_wrong_product_type(self):
        """Cannot link to a product with a wrong type."""
        self.product.event_type_id = self.event_type_1
        self.event.type = self.event_type_2
        with self.assertRaises(ex.TypeMismatchError):
            self.event.product_id = self.product

    def test_onchange_type_remove_wrong_product(self):
        """Onchange avoids conflict with wrong product type."""
        self.product.event_type_id = self.event_type_1
        self.event_new.type = self.event_type_1
        self.event_new._onchange_type_clear_product()
        self.event_new.product_id = self.product
        self.event_new.type = self.event_type_2
        self.event_new._onchange_type_clear_product()
        self.assertFalse(self.event.product_id)
