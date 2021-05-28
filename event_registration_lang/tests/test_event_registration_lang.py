# Copyright 2021 Camptocamp (https://www.camptocamp.com).
# @author Iván Todorovich <ivan.todorovich@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import SavepointCase


class TestEventRegistrationLang(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.event = cls.env.ref("event.event_0")
        cls.partner = cls.env.ref("base.res_partner_1")
        cls.env["res.lang"].load_lang("fr_FR")

    def test_01_onchange(self):
        registration = self.env["event.registration"].create(
            {"event_id": self.event.id, "partner_id": self.partner.id}
        )
        self.assertEqual(self.partner.lang, registration.lang)

    def test_02_prepare_attendee_values(self):
        EventRegistration = self.env["event.registration"]
        vals = {
            "event_id": self.event,
            "partner_id": self.partner,
            "name": "John Doe",
            "lang": "fr_FR",
        }
        registration = EventRegistration.create(
            EventRegistration._prepare_attendee_values(vals)
        )
        self.assertEqual(registration.lang, "fr_FR")
