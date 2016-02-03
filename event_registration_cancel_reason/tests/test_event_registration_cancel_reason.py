# -*- coding: utf-8 -*-
# © 2016 Antiun Ingeniería S.L.
# © 2016 Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import fields
from openerp.tests import common


class TestEventRegistrationCancelReason(common.TransactionCase):
    def setUp(self):
        super(TestEventRegistrationCancelReason, self).setUp()
        self.event = self.env['event.event'].create(
            {'name': 'Test event',
             'date_begin': fields.Date.today(),
             'date_end': fields.Date.today()})
        self.partner = self.env['res.partner'].create({'name': 'Test partner'})
        self.cancel_reason = self.env[
            'event.registration.cancel.reason'].create({'name': 'Test reason'})
        self.registration = self.env['event.registration'].create(
            {'event_id': self.event.id,
             'partner_id': self.partner.id})

    def test_cancel(self):
        action = self.registration.button_reg_cancel()
        self.assertEqual(action.get('type'), 'ir.actions.act_window')
        wizard_model = self.env['event.registration.cancel.log.reason']
        wizard = wizard_model.with_context(
            active_id=self.registration.id).create(
            {'reason_id': self.cancel_reason.id})
        wizard.button_log()
        self.assertEqual(
            self.registration.cancel_reason_id, self.cancel_reason)
