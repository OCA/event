# -*- coding: utf-8 -*-
# Copyright 2016 Antiun Ingenieria S.L. - Javier Iniesta
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp.tests.common import TransactionCase


class TestEventRegistrationMailListWizard(TransactionCase):

    def setUp(self):
        super(TestEventRegistrationMailListWizard, self).setUp()
        self.mass_mailing_obj = self.env['mail.mass_mailing']
        self.mail_list = self.env['mail.mass_mailing.list'].create({
            'name': 'Test 01'})
        self.contact = self.env['mail.mass_mailing.contact'].create({
            'name': 'Test Contact 01', 'email': 'email01@test.com',
            'list_id': self.mail_list.id})
        self.event = self.env.ref('event.event_0')
        self.registration_01 = self.env['event.registration'].create({
            'name': 'Test Registration 01', 'email': 'email01@test.com',
            'event_id': self.event.id})
        self.registration_02 = self.env['event.registration'].create({
            'name': 'Test Registration 02', 'email': 'email02@test.com',
            'event_id': self.event.id})

    def test_add_to_mail_list(self):
        wizard = self.env['event.registration.mail.list.wizard'].create({
            'mail_list': self.mail_list.id})
        wizard.with_context(
            {'active_ids': [self.registration_01.id,
                            self.registration_02.id]}).add_to_mail_list()

        self.assertEqual(self.mail_list.contact_nbr, 2)
        mass_mailing = self.mass_mailing_obj.search(
            [('contact_list_ids', 'in', [self.mail_list.id])])
        models = mass_mailing._get_mailing_model()
        models_list = [x[0] for x in models]
        self.assertTrue('event.registration' in models_list)
