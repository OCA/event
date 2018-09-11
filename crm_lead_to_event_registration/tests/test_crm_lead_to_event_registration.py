# Copyright 2016 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields
from odoo.tests import common


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
        self.wiz_event = self.env['crm.lead.event.pick'].with_context(
            active_ids=[self.lead.id], active_id=self.lead.id,
            active_model='crm.lead'
        )

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

    def test_event_pick_and_track(self):
        stage_won = self.env.ref('crm.stage_lead4')
        wizard = self.wiz_event.create({
            'lead_id': self.lead.id,
            'event_id': self.event.id,
        })
        wizard.action_accept()
        self.assertTrue(self.event.registration_ids)

        def _track_subtype(self, init_values):
            self.ensure_one()
            if 'stage_id' in init_values \
                    and self.probability == 100 \
                    and self.stage_id \
                    and self.stage_id.on_change:
                return 'crm.mt_lead_won'
            elif 'active' in init_values \
                    and self.probability == 0 and not self.active:
                return 'crm.mt_lead_lost'
            return False

        self.registry('crm.lead')._patch_method(
            '_track_subtype', _track_subtype)
        self.lead.stage_id = stage_won
        self.assertEqual(
            self.lead._track_subtype(['stage_id']), 'crm.mt_lead_won')
        self.lead.write({
            'active': False,
            'probability': 0,
        })
        self.assertEqual(
            self.lead._track_subtype(['active']), 'crm.mt_lead_lost')
