# Copyright 2016 Antiun Ingeniería S.L. - Jairo Llopis
# Copyright 2020 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase

from .. import exceptions


class DuplicatedPartnerCase(TransactionCase):
    def setUp(self):
        super().setUp()
        self.event = self.env.ref("event.event_0")
        self.event.forbid_duplicates = False
        self.partner = self.env.ref("base.res_partner_1")
        self.registration = self.env["event.registration"].create(
            {
                "event_id": self.event.id,
                "partner_id": self.partner.id,
                "attendee_partner_id": self.partner.id,
            }
        )

    def test_allowed(self):
        """No problem when it is not forbidden."""
        self.registration.copy()

    def test_forbidden(self):
        """Cannot when it is forbidden."""
        self.event.forbid_duplicates = True
        with self.assertRaises(exceptions.DuplicatedPartnerError):
            self.registration.copy(
                {"attendee_partner_id": self.registration.attendee_partner_id.id}
            )

    def test_saved_in_exception(self):
        """The failing partners are saved in the exception."""
        self.event.forbid_duplicates = True
        try:
            self.registration.copy(
                {"attendee_partner_id": self.registration.attendee_partner_id.id}
            )
        except exceptions.DuplicatedPartnerError as error:
            self.assertEqual(error._kwargs["registrations"], self.registration)

    def test_duplicates_already_exist(self):
        """Cannot forbid what already happened."""
        self.registration.copy(
            {"attendee_partner_id": self.registration.attendee_partner_id.id}
        )
        with self.assertRaises(exceptions.DuplicatedPartnerError):
            self.event.forbid_duplicates = True
