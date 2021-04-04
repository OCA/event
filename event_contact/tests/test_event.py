# Copyright 2016-2017 Jairo Llopis <jairo.llopis@tecnativa.com>
# Copyright 2019 Alexandre Díaz <alexandre.diaz@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp.tests.common import TransactionCase


class EventCase(TransactionCase):
    def setUp(self, *args, **kwargs):
        super(EventCase, self).setUp(*args, **kwargs)

        # Partners
        self.partner1 = self.env["res.partner"].create({"name": "Test Partner 1"})
        self.partner2 = self.env["res.partner"].create({"name": "Test Partner 2"})
        self.partner3 = self.env["res.partner"].create({"name": "Test Partner 3"})
        self.partner4 = self.env["res.partner"].create({"name": "Test Partner 4"})
        self.partner5 = self.env["res.partner"].create({"name": "Test Partner 5"})

        self.type1 = self.env["event.type"].create(
            {
                "name": "Event Type Test 1",
                "contact_ids": [(6, False, [self.partner1.id, self.partner2.id])],
            }
        )
        self.type2 = self.env["event.type"].create(
            {
                "name": "Event Type Test 2",
                "contact_ids": [(6, False, [self.partner3.id, self.partner4.id])],
            }
        )

        self.event1 = self.env["event.event"].create(
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
        self.event1.contact_ids = [(6, False, [self.partner5.id])]
        self.event1.event_type_id = self.type1
        self.assertEqual(
            self.event1.contact_ids, self.partner5 | self.type1.contact_ids
        )
