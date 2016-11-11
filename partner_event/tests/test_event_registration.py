# -*- coding: utf-8 -*-
# © 2014 Serv. Tecnol. Avanzados - Pedro M. Baeza
# © 2015 Antiun Ingenieria S.L. - Javier Iniesta
# © 2016 Antiun Ingenieria S.L. - Antonio Espinosa
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class TestEventRegistration(TransactionCase):

    def setUp(self):
        super(TestEventRegistration, self).setUp()
        self.event_0 = self.env.ref('event.event_0')
        self.event_0.create_partner = True
        registration_model = self.env['event.registration']
        partner_model = self.env['res.partner']
        self.partner_01 = partner_model.create({'name': 'Test Partner 01',
                                                'email': 'email01@test.com'})
        self.registration_01 = registration_model.create({
            'email': 'email01@test.com', 'event_id': self.event_0.id})
        self.registration_02 = registration_model.create({
            'email': 'email02@test.com', 'event_id': self.event_0.id,
            'name': 'Test Registration 02', 'phone': '254728911'})

    def test_create(self):
        self.assertEqual(self.partner_01.name, self.registration_01.name)
        self.assertEqual(self.partner_01.email, self.registration_01.email)
        self.assertEqual(self.partner_01.phone, self.registration_01.phone)
        partner_02 = self.registration_02.partner_id
        self.assertEqual(partner_02.name, self.registration_02.name)
        self.assertEqual(partner_02.email, self.registration_02.email)
        self.assertEqual(partner_02.phone, self.registration_02.phone)

    def test_count_events(self):
        event_1 = self.event_0.copy()
        self.assertEqual(self.partner_01.event_count, 0)
        self.registration_01.state = "open"
        self.partner_01.invalidate_cache()
        self.assertEqual(self.partner_01.event_count, 1)
        self.registration_02.state = "done"
        self.registration_02.partner_id = self.partner_01
        self.registration_02.event_id = event_1
        self.partner_01.invalidate_cache()
        self.assertEqual(self.partner_01.event_count, 2)

    def test_button_register(self):
        event_1 = self.env.ref('event.event_1')
        wizard = self.env['res.partner.register.event'].create({
            'event': event_1.id})
        active_ids = [self.partner_01.id, self.registration_02.partner_id.id]
        wizard.with_context({'active_ids': active_ids}).button_register()
