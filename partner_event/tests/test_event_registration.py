# Copyright 2014 Tecnativa S.L. - Pedro M. Baeza
# Copyright 2015 Tecnativa S.L. - Javier Iniesta
# Copyright 2016 Tecnativa S.L. - Antonio Espinosa
# Copyright 2016 Tecnativa S.L. - Vicent Cubells
# Copyright 2017 Tecnativa - David Vidal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import datetime, timedelta

from psycopg2 import IntegrityError

from odoo import fields
from odoo.tests import common


class TestEventRegistration(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestEventRegistration, cls).setUpClass()
        cls.event_0 = cls.env["event.event"].create(
            {
                "name": "Test event",
                "date_begin": fields.Datetime.now(),
                "date_end": fields.Datetime.now(),
                "seats_limited": True,
                "seats_max": "5",
            }
        )
        cls.event_0.create_partner = True
        registration_model = cls.env["event.registration"].with_context(
            registration_force_draft=True
        )
        partner_model = cls.env["res.partner"]
        cls.partner_01 = partner_model.create(
            {
                "name": "Test Partner 01",
                "email": "email01@test.com",
                "phone": "254728911",
            }
        )
        cls.registration_01 = registration_model.create(
            {"email": "email01@test.com", "event_id": cls.event_0.id}
        )
        cls.registration_02 = registration_model.create(
            {
                "email": "email02@test.com",
                "event_id": cls.event_0.id,
                "name": "Test Registration 02",
                "phone": "254728911",
            }
        )

    def test_create(self):
        self.assertEqual(self.partner_01.name, self.registration_01.name)
        self.assertEqual(self.partner_01.email, self.registration_01.email)
        self.assertEqual(self.partner_01.phone, self.registration_01.phone)
        partner_02 = self.registration_02.attendee_partner_id
        self.assertEqual(partner_02.name, self.registration_02.name)
        self.assertEqual(partner_02.email, self.registration_02.email)
        self.assertEqual(partner_02.phone, self.registration_02.phone)

    def test_count_registrations(self):
        event_1 = self.event_0.copy()
        self.assertEqual(self.partner_01.registration_count, 0)
        self.registration_01.state = "open"
        self.partner_01.invalidate_cache()
        self.assertEqual(self.partner_01.registration_count, 1)
        self.registration_02.state = "done"
        self.registration_02.attendee_partner_id = self.partner_01
        self.registration_02.event_id = event_1
        self.partner_01.invalidate_cache()
        self.assertEqual(self.partner_01.registration_count, 2)

    def test_button_register(self):
        event_1 = self.event_0.copy()
        wizard = self.env["res.partner.register.event"].create({"event": event_1.id})
        active_ids = [self.partner_01.id, self.registration_02.attendee_partner_id.id]
        wizard.with_context({"active_ids": active_ids}).button_register()

    def test_data_update(self):
        event_2 = self.event_0.copy()
        self.yesterday = datetime.now() - timedelta(days=1)
        self.tomorrow = datetime.now() + timedelta(days=1)
        self.last_moth = datetime.now() - timedelta(days=30)
        # Set an old event
        event_2.write({"date_begin": self.last_moth})
        event_2.write({"date_end": self.yesterday})
        self.registration_02.event_id = event_2
        self.registration_02.attendee_partner_id = self.partner_01
        # Update partner for an old event
        self.partner_01.write({"email": "new@test.com"})
        self.assertNotEqual(event_2.registration_ids.email, "new@test.com")
        # Update partner for an current event
        event_2.write({"date_end": self.tomorrow})
        self.partner_01.write({"email": "new@test.com"})
        self.assertEqual(event_2.registration_ids.email, "new@test.com")

    def test_delete_registered_partner(self):
        # We can't delete a partner with registrations
        with self.assertRaises(IntegrityError), self.cr.savepoint():
            self.cr._default_log_exceptions = False
            self.partner_01.unlink()
        # Create a brand new partner and delete it
        partner3 = self.env["res.partner"].create({"name": "unregistered partner"})
        partner3.unlink()
        self.assertFalse(partner3.exists())
