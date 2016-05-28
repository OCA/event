# -*- coding: utf-8 -*-
# © 2016 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields
from openerp.tests import common


class TestEventProject(common.TransactionCase):
    def setUp(self):
        super(TestEventProject, self).setUp()
        self.project = self.env['project.project'].create({
            'name': 'Test project',
        })
        self.event = self.env['event.event'].create({
            'name': 'Test event',
            'date_begin': fields.Datetime.now(),
            'date_end': fields.Datetime.now(),
            'project_id': self.project.id,
        })

    def test_cancel_event(self):
        self.event.button_cancel()
        self.assertEqual(self.project.state, 'cancelled')
