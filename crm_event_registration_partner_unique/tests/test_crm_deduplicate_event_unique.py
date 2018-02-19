# -*- coding: utf-8 -*-
# Copyright 2018 Tecnativa - David Vidal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests import common
from openerp.exceptions import UserError


class TestDeduplicateEventUnique(common.TransactionCase):
    def setUp(self):
        super(TestDeduplicateEventUnique, self).setUp()
        self.partner_1 = self.env['res.partner'].create({
            'name': 'Partner 1',
        })
        self.partner_2 = self.env['res.partner'].create({
            'name': 'Partner 2',
        })
        self.event = self.env['event.event'].create({
            'name': 'Test event',
            'date_begin': '2018-01-11 15:20:00',
            'date_end': '2018-01-11 22:00:00',
            'seats_availability': 'unlimited',
        })
        self.registration_1 = self.env["event.registration"].create({
            "event_id": self.event.id,
            "partner_id": self.partner_1.id,
        })
        self.registration_2 = self.env["event.registration"].create({
            "event_id": self.event.id,
            "partner_id": self.partner_2.id,
        })
        self.wizard = self.env['base.partner.merge.automatic.wizard'].create({
            'dst_partner_id': self.partner_1.id,
            'partner_ids': [(4, self.partner_1.id), (4, self.partner_2.id)],
            'group_by_name': True,
        })

    def test_01_merge_forbidden_event(self):
        self.event.forbid_duplicates = True
        with self.assertRaises(UserError):
            self.wizard.merge_cb()

    def test_02_merge_allowed_event(self):
        self.wizard.merge_cb()
        self.assertEqual(self.event.registration_ids.mapped('partner_id').id,
                         self.partner_1.id)
