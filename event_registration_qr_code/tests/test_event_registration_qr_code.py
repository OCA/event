# Copyright 2022 Moka Tourisme (https://www.mokatourisme.fr).
# @author Iván Todorovich <ivan.todorovich@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from psycopg2.errors import UniqueViolation

from odoo.tests.common import TransactionCase
from odoo.tools import mute_logger


class TestEventRegistrationQrCode(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.event = cls.env.ref("event.event_0")

    def test_01_qr_code_generate(self):
        event_registration = self.env["event.registration"].create(
            {
                "event_id": self.event.id,
                "name": "Test Registration",
            }
        )
        self.assertTrue(event_registration.qr_code)

    @mute_logger("odoo.sql_db")
    def test_02_qr_code_unique(self):
        registration_1, registration_2 = self.env["event.registration"].create(
            [
                {
                    "event_id": self.event.id,
                    "name": "Test Registration 1",
                },
                {
                    "event_id": self.event.id,
                    "name": "Test Registration 2",
                },
            ]
        )
        with self.assertRaisesRegex(
            UniqueViolation, "event_registration_qr_code_unique"
        ):
            registration_1.qr_code = registration_2.qr_code
            registration_1.flush_recordset()
