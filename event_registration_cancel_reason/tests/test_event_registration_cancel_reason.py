# Copyright 2016 Antiun Ingeniería S.L.
# Copyright 2016 Tecnativa - Pedro M. Baeza
# Copyright 2017 Tecnativa - Vicent Cubells
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import exceptions, fields
from odoo.tests import common


class TestEventRegistrationCancelReason(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.event1 = cls.env["event.event"].create(
            {
                "name": "Test event",
                "event_type_id": cls.env.ref("event.event_type_1").id,
                "date_begin": fields.Date.today(),
                "date_end": fields.Date.today(),
            }
        )
        cls.event2 = cls.event1.copy()
        cls.partner = cls.env["res.partner"].create({"name": "Test partner"})
        cls.cancel_reason = cls.env["event.registration.cancel.reason"].create(
            {"name": "Test reason"}
        )
        cls.registration1 = cls.env["event.registration"].create(
            {"event_id": cls.event1.id, "partner_id": cls.partner.id}
        )
        cls.registration2 = cls.registration1.copy()
        cls.registration2.event_id = cls.event2
        cls.registrations = cls.registration1 | cls.registration2
        cls.wizard_model = cls.env["event.registration.cancel.log.reason"]

    def test_cancel(self):
        action = self.registration1.action_cancel()
        self.assertEqual(action.get("type"), "ir.actions.act_window")
        wizard = self.wizard_model.with_context(
            active_ids=self.registrations.ids
        ).create({"reason_id": self.cancel_reason.id})
        wizard.button_log()
        self.assertEqual(self.registration1.cancel_reason_id, self.cancel_reason)
        self.registration1.action_set_draft()
        self.assertFalse(self.registration1.cancel_reason_id)

    def test_cancel_multi_event_type(self):
        """Registration cancel from different event types are aborted."""
        self.event2.event_type_id = self.env.ref("event.event_type_2")
        with self.assertRaises(exceptions.ValidationError):
            self.wizard_model.with_context(active_ids=self.registrations.ids).create(
                {"reason_id": self.cancel_reason.id}
            )

    def test_cancel_one_event_without_type(self):
        """Registration cancel from 2 events (1 typed, 1 not) are aborted."""
        self.event2.event_type_id = False
        with self.assertRaises(exceptions.ValidationError):
            self.wizard_model.with_context(active_ids=self.registrations.ids).create(
                {"reason_id": self.cancel_reason.id}
            )
