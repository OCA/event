# -*- coding: utf-8 -*-
# © 2016 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import fields
from openerp.tests import common


class TestCrmLeadToEventRegistration(common.TransactionCase):
    def setUp(self):
        super(TestCrmLeadToEventRegistration, self).setUp()
        self.lead = self.env['crm.lead'].create({
            'name': 'Test lead',
            'partner_name': 'Test',
        })
        self.event = self.env['event.event'].create(
            {'name': 'Test event',
             'date_begin': fields.Date.today(),
             'date_end': fields.Date.today()})
        self.partner = self.env['res.partner'].create({'name': 'Test partner'})
        self.registration = self.env['event.registration'].create(
            {'event_id': self.event.id,
             'partner_id': self.partner.id})
        self.wiz_obj = self.env['crm.lead2opportunity.partner'].with_context(
            active_ids=[self.lead.id], active_id=self.lead.id,
            active_model='crm.lead')

    def test_convert_lead_wo_partner(self):
        wizard = self.wiz_obj.create({
            'event_id': self.event.id,
            'name': 'convert',
            'action': 'create',
        })
        wizard.action_apply()
        self.assertTrue(self.event.registration_ids)
        self.assertTrue(self.event.registration_ids[0].partner_id)

    def test_convert_lead_with_partner(self):
        wizard = self.wiz_obj.create({
            'event_id': self.event.id,
            'name': 'convert',
            'action': 'exist',
            'partner_id': self.partner.id,
        })
        wizard.action_apply()
        self.assertTrue(self.event.registration_ids)
        self.assertEqual(
            self.event.registration_ids[0].partner_id, self.partner)
