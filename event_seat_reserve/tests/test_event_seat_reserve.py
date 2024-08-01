# Copyright 2024 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestEventSeatReserve(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        test_context = cls.env.context.copy()
        test_context["test_event_seat_reserve"] = True
        cls.env = cls.env(context=dict(test_context, tracking_disable=True))
        # ../event/data/event_demo.xml
        # using this demo data, we have a max_seats = 4
        # and 3 registrations
        cls.event = cls.env.ref("event.event_4")
        cls.partner = cls.env.ref("base.res_partner_1")
        cls.registration = cls.env["event.registration"].create(
            {
                "event_id": cls.event.id,
                "partner_id": cls.partner.id,
            }
        )

    def test_01_reserved_quantity(self):
        """
        Test that reserved quantity is set and if seats are available or not
        """
        # ../event/data/event_demo.xml
        self.assertEqual(self.event.seats_max, 4)

        self.assertEqual(self.event.seats_expected, 4)
        self.assertEqual(self.event.seats_available, 1)
        self.assertEqual(self.event.seats_reserved_unconfirmed, 0)
        self.registration.action_set_reserved()
        self.assertEqual(self.event.seats_reserved_unconfirmed, 1)

        self.assertEqual(self.event.seats_available, 0)

    def test_02_reserve_more_than_available(self):
        """
        Test that we can't reserve more than available seats
        """
        self.registration.action_set_reserved()
        registration2 = self.env["event.registration"].create(
            {
                "event_id": self.event.id,
                "name": "Test",
            }
        )
        with self.assertRaises(ValidationError):
            registration2.action_set_reserved()
