# -*- coding: utf-8 -*-
# © 2015 Grupo ESOC Ingeniería de Servicios, S.L.U. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


class BaseCase(object):
    def setUp(self, *args, **kwargs):
        result = super(BaseCase, self).setUp(*args, **kwargs)

        self.product = self.env["product.product"].create({
            "name": u"Test ëvent 1",
            "is_event": True,
        })
        self.deliverable_product_1 = self.env["product.product"].create({
            "name": u"Têst deliverable 1",
        })
        self.deliverable_product_2 = self.env["product.product"].create({
            "name": u"Têst deliverable 2",
        })
        self.deliverable_products = (self.deliverable_product_1 |
                                     self.deliverable_product_2)
        self.event = self.env["event.event"].create({
            "name": u"Some evént.",
            "date_begin": "2015-11-26",
            "date_end": "2015-11-30",
        })
        self.event_registration = self.env["event.registration"].create({
            "name": u"Some registratioǹ",
            "event_id": self.event.id,
        })

        return result
