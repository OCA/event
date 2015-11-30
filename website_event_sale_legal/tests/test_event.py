# -*- coding: utf-8 -*-
# © 2015 Antiun Ingeniería, S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class EventCase(TransactionCase):
    def setUp(self, *args, **kwargs):
        result = super(EventCase, self).setUp(*args, **kwargs)

        self.lt1 = self.env["website_sale_product_legal.legal_term"].create({
            "name": u"LËgal term 1",
            "contents": u"Sômething",
        })
        self.lt2 = self.env["website_sale_product_legal.legal_term"].create({
            "name": u"LËgal term 2",
            "contents": u"Sômething",
        })
        self.lt3 = self.env["website_sale_product_legal.legal_term"].create({
            "name": u"LËgal term 3",
            "contents": u"Sômething",
        })
        self.event = self.env["event.event"].create({
            "name": u"Evént 1",
            "date_begin": "2015-11-30 09:00:00",
            "date_end": "2015-12-30 09:00:00",
        })
        self.ticket_product = self.env["product.product"].create({
            "name": u"Tickét prodúct 1",
            "event_ok": True,
        })
        self.ticket = self.env["event.event.ticket"].create({
            "name": u"Tícket 1",
            "product_id": self.ticket_product.id,
            "event_id": self.event.id,
        })

        return result

    def test_mixed_legal_terms(self):
        """Legal terms get correctly mixed."""
        self.ticket_product.legal_term_ids = self.lt1
        self.event.legal_term_ids = self.lt2
        self.ticket.legal_term_ids = self.lt3

        self.assertEqual(
            self.ticket.mixed_legal_term_ids,
            self.lt1 | self.lt2 | self.lt3)
