# Copyright 2016-2017 Jairo Llopis <jairo.llopis@tecnativa.com>
# Copyright 2019 Alexandre Díaz <alexandre.diaz@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import Command
from odoo.tests.common import TransactionCase


class EventCase(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Partners
        cls.partner1 = cls.env["res.partner"].create({"name": "Test Partner 1"})
        cls.partner2 = cls.env["res.partner"].create({"name": "Test Partner 2"})
        cls.partner3 = cls.env["res.partner"].create({"name": "Test Partner 3"})
        cls.partner4 = cls.env["res.partner"].create({"name": "Test Partner 4"})
        cls.partner5 = cls.env["res.partner"].create({"name": "Test Partner 5"})

        cls.type1 = cls.env["event.type"].create(
            {
                "name": "Event Type Test 1",
                "contact_ids": [Command.set([cls.partner1.id, cls.partner2.id])],
            }
        )
        cls.type2 = cls.env["event.type"].create(
            {
                "name": "Event Type Test 2",
                "contact_ids": [Command.set([cls.partner3.id, cls.partner4.id])],
            }
        )

        cls.event1 = cls.env["event.event"].create(
            {
                "name": "Event Test 1",
                "date_begin": "2019-06-20",
                "date_end": "2019-06-23",
            }
        )

    def test_event_onchange_type_contacts_empty(self):
        """You get default contacts from type."""
        self.event1.event_type_id = self.type2
        self.assertEqual(self.event1.contact_ids, self.type2.contact_ids)

    def test_event_onchange_type_contacts_full(self):
        """Contacts not updated because it is not empty."""
        self.event1.contact_ids = [Command.set([self.partner5.id])]
        self.event1.event_type_id = self.type1
        self.assertEqual(
            self.event1.contact_ids, self.partner5 | self.type1.contact_ids
        )
