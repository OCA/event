# -*- coding: utf-8 -*-
# © 2016 Antiun Ingeniería S.L.
# © 2016 Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import exceptions, fields
from openerp.tests import common


class TestEventRegistrationCancelReason(common.TransactionCase):
    def setUp(self):
        super(TestEventRegistrationCancelReason, self).setUp()
        self.event1 = self.env['event.event'].create(
            {'name': 'Test event',
             'type': self.env.ref('event.event_type_1').id,
             'date_begin': fields.Date.today(),
             'date_end': fields.Date.today()})
        self.event2 = self.event1.copy()
        self.partner = self.env['res.partner'].create({'name': 'Test partner'})
        self.cancel_reason = self.env[
            'event.registration.cancel.reason'].create({'name': 'Test reason'})
        self.registration1 = self.env['event.registration'].create(
            {'event_id': self.event1.id,
             'partner_id': self.partner.id})
        self.registration2 = self.registration1.copy()
        self.registration2.event_id = self.event2
        self.registrations = self.registration1 | self.registration2
        self.wizard_model = self.env['event.registration.cancel.log.reason']

    def test_cancel(self):
        action = self.registration1.button_reg_cancel()
        self.assertEqual(action.get('type'), 'ir.actions.act_window')
        wizard = self.wizard_model.with_context(
            active_ids=self.registrations.ids).create(
            {'reason_id': self.cancel_reason.id})
        wizard.button_log()
        self.assertEqual(
            self.registration1.cancel_reason_id, self.cancel_reason)

    def test_cancel_multi_event_type(self):
        """Registration cancel from different event types are aborted."""
        self.event2.type = self.env.ref("event.event_type_2")
        with self.assertRaises(exceptions.ValidationError):
            self.wizard_model.with_context(
                active_ids=self.registrations.ids).create(
                {'reason_id': self.cancel_reason.id})

    def test_cancel_one_event_without_type(self):
        """Registration cancel from 2 events (1 typed, 1 not) are aborted."""
        self.event2.type = False
        with self.assertRaises(exceptions.ValidationError):
            self.wizard_model.with_context(
                active_ids=self.registrations.ids).create(
                {'reason_id': self.cancel_reason.id})
