# Copyright 2016 Antiun Ingenieria S.L. - Javier Iniesta
# Copyright 2020 Tecnativa - David Vidal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields
from odoo.tests.common import SavepointCase


class TestEventRegistrationMailListWizard(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.mass_mailing_obj = cls.env["mailing.mailing"]
        cls.mail_list = cls.env["mailing.list"].create({"name": "Test 01"})
        cls.contact = cls.env["mailing.contact"].create(
            {
                "name": "Test Contact 01",
                "email": "email01@test.com",
                "list_ids": [[6, 0, [cls.mail_list.id]]],
            }
        )
        cls.event = cls.env["event.event"].create(
            {
                "name": "Test event",
                "date_begin": fields.Datetime.now(),
                "date_end": fields.Datetime.now(),
                "seats_max": "5",
            }
        )
        cls.registration_01 = cls.env["event.registration"].create(
            {
                "name": "Test Registration 01",
                "email": "email01@test.com",
                "event_id": cls.event.id,
            }
        )
        cls.registration_02 = cls.env["event.registration"].create(
            {
                "name": "Test Registration 02",
                "email": "email02@test.com",
                "event_id": cls.event.id,
            }
        )

    def test_add_to_mail_list(self):
        wizard = self.env["event.registration.mail.list.wizard"].create(
            {"mail_list": self.mail_list.id}
        )
        wizard.with_context(
            {"active_ids": [self.registration_01.id, self.registration_02.id]}
        ).add_to_mail_list()
        self.assertEqual(len(self.mail_list.contact_ids), 2)
