# -*- coding: utf-8 -*-
# © 2016 Antiun Ingeniería S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp.tests.common import TransactionCase


class SomethingCase(TransactionCase):
    def setUp(self, *args, **kwargs):
        super(SomethingCase, self).setUp(*args, **kwargs)
        self.type1 = self.env.ref("event.event_type_1")
        self.type2 = self.env.ref("event.event_type_2")
        self.type1.contact_ids = (
            self.env.ref("base.res_partner_1") |
            self.env.ref("base.res_partner_2"))
        self.type2.contact_ids = (
            self.env.ref("base.res_partner_3") |
            self.env.ref("base.res_partner_4"))

        self.event1 = self.env.ref("event.event_1")

    def test_event_onchange_type_contacts_empty(self):
        """You get default contacts from type."""
        self.event1.type = self.type2
        self.event1._onchange_type_set_contact_ids()
        self.assertEqual(self.event1.contact_ids, self.type2.contact_ids)

    def test_event_onchange_type_contacts_full(self):
        """Contacts not updated because it is not empty."""
        self.event1.type = self.type1
        self.event1._onchange_type_set_contact_ids()
        self.event1.type = self.type2
        self.event1._onchange_type_set_contact_ids()
        self.assertEqual(self.event1.contact_ids, self.type1.contact_ids)
