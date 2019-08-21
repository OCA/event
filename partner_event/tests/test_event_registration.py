# -*- coding: utf-8 -*-
# © 2014 Tecnativa S.L. - Pedro M. Baeza
# © 2015 Tecnativa S.L. - Javier Iniesta
# © 2016 Tecnativa S.L. - Antonio Espinosa
# © 2016 Tecnativa S.L. - Vicent Cubells
# Copyright 2017 Tecnativa - David Vidal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from psycopg2 import IntegrityError
from datetime import datetime, timedelta
from odoo.tests import common
from odoo import fields
from ..hooks import LANG_NEW, LANG_OLD, uninstall_hook


class TestEventRegistration(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestEventRegistration, cls).setUpClass()
        cls.demo_user = cls.env.ref("base.user_demo")
        cls.demo_user.groups_id -= cls.env.ref("event.group_event_user")
        cls.event_0 = cls.env['event.event'].create({
            'name': 'Test event',
            'date_begin': fields.Datetime.now(),
            'date_end': fields.Datetime.now(),
            'seats_availability': 'limited',
            'seats_max': '5',
            'seats_min': '1',
        })
        cls.event_0.create_partner = True
        registration_model = cls.env[
            'event.registration'].with_context(registration_force_draft=True)
        partner_model = cls.env['res.partner']
        cls.partner_01 = partner_model.create({
            'name': 'Test Partner 01',
            'email': 'email01@test.com'
        }).sudo(cls.demo_user)
        cls.registration_01 = registration_model.create({
            'email': 'email01@test.com', 'event_id': cls.event_0.id})
        cls.registration_02 = registration_model.create({
            'email': 'email02@test.com', 'event_id': cls.event_0.id,
            'name': 'Test Registration 02', 'phone': '254728911'})
        # Need a 2nd lang to do some lang-specific tests
        wiz = cls.env["base.language.install"].create({
            "lang": "it_IT",
        })
        wiz.lang_install()

    def test_create(self):
        self.assertEqual(self.partner_01.name, self.registration_01.name)
        self.assertEqual(self.partner_01.email, self.registration_01.email)
        self.assertEqual(self.partner_01.phone, self.registration_01.phone)
        partner_02 = self.registration_02.attendee_partner_id
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
        self.registration_02.attendee_partner_id = self.partner_01
        self.registration_02.event_id = event_1
        self.partner_01.invalidate_cache()
        self.assertEqual(self.partner_01.event_count, 2)

    def test_button_register(self):
        event_1 = self.event_0.copy()
        wizard = self.env['res.partner.register.event'].create({
            'event': event_1.id})
        active_ids = [
            self.partner_01.id, self.registration_02.attendee_partner_id.id]
        wizard.with_context({'active_ids': active_ids}).button_register()

    def test_data_update(self):
        event_2 = self.event_0.copy()
        self.yesterday = datetime.now() - timedelta(days=1)
        self.tomorrow = datetime.now() + timedelta(days=1)
        self.last_moth = datetime.now() - timedelta(days=30)
        # Set an old event
        event_2.write({'date_begin': self.last_moth})
        event_2.write({'date_end': self.yesterday})
        self.registration_02.event_id = event_2
        self.registration_02.attendee_partner_id = self.partner_01
        # Update partner for an old event
        self.partner_01.write({'email': 'new@test.com'})
        self.assertNotEqual(
            event_2.registration_ids.email, 'new@test.com')
        # Update partner for an current event
        event_2.write({'date_end': self.tomorrow})
        self.partner_01.write({'email': 'new@test.com'})
        self.assertEqual(
            event_2.registration_ids.email, 'new@test.com')

    def test_delete_registered_partner(self):
        # We can't delete a partner with registrations
        with self.assertRaises(IntegrityError), self.cr.savepoint():
            self.partner_01.unlink()
        # Create a brand new partner and delete it
        partner3 = self.env['res.partner'].create({
            'name': 'unregistered partner',
        })
        partner3.unlink()
        self.assertFalse(partner3.exists())

    def test_badge_email_lang(self):
        """Attendee created in right lang, badge generated in such."""
        # Attendee should be created with Spanish language
        reg3 = self.env["event.registration"] \
            .with_context(lang="it_IT").create({
                'email': 'email03@test.com',
                'event_id': self.event_0.id
            })
        reg3 = reg3.with_context(lang="en_US")
        self.assertEqual(reg3.attendee_partner_id.lang, "it_IT")
        # Badge should be printed in Spanish, no matter user's context
        action = reg3.action_send_badge_email()
        self.assertEqual(action["context"]["lang"], "it_IT")

    def test_message_recipient_suggestion(self):
        """Attendee partner is suggested as follower."""
        suggestions = self.registration_02.message_get_suggested_recipients()
        self.assertNotIn(
            self.partner_01.id,
            {each[0] for each in suggestions[self.registration_02.id]},
        )
        self.assertIn(
            self.registration_02.attendee_partner_id.id,
            {each[0] for each in suggestions[self.registration_02.id]},
        )
        # Partner 01 pays the bill
        self.registration_02.partner_id = self.partner_01
        suggestions = self.registration_02.message_get_suggested_recipients()
        self.assertIn(
            self.partner_01.id,
            {each[0] for each in suggestions[self.registration_02.id]},
        )
        self.assertIn(
            self.registration_02.attendee_partner_id.id,
            {each[0] for each in suggestions[self.registration_02.id]},
        )

    def test_uninstall_hook(self):
        """Lang in templates is restored after uninstall"""
        # All templates must have new lang computing
        tpls = self.env["mail.template"].search([
            ("model_id", "=", "event.registration"),
            ("lang", "=", LANG_NEW),
        ])
        self.assertTrue(tpls)
        tpls = self.env["mail.template"].search([
            ("model_id", "=", "event.registration"),
            ("lang", "=", LANG_OLD),
        ])
        self.assertFalse(tpls)
        # Uninstall
        uninstall_hook(self.env.cr, None)
        # All templates must have old lang computing
        tpls = self.env["mail.template"].search([
            ("model_id", "=", "event.registration"),
            ("lang", "=", LANG_NEW),
        ])
        self.assertFalse(tpls)
        tpls = self.env["mail.template"].search([
            ("model_id", "=", "event.registration"),
            ("lang", "=", LANG_OLD),
        ])
        self.assertTrue(tpls)
