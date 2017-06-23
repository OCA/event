# -*- coding: utf-8 -*-
# Copyright 2016 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# Copyright 2017 David Vidal <david.vidal@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields
from odoo.tests import common
from datetime import timedelta, date


class TestEventProject(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestEventProject, cls).setUpClass()
        cls.date = {
            'begin': fields.Date.to_string(date.today()),
            'end': fields.Date.to_string(date.today() + timedelta(days=7)),
            'begin2': fields.Date.to_string(date.today() + timedelta(days=1)),
            'end2': fields.Date.to_string(date.today() + timedelta(days=9)),
        }
        cls.project = cls.env['project.project'].create({
            'name': 'Test project',
        })
        cls.project_2 = cls.env['project.project'].create({
            'name': 'Test project 2',
        })
        cls.event = cls.env['event.event'].create({
            'name': 'Test event with project',
            'date_begin': cls.date['begin'],
            'date_end': cls.date['end'],
            'project_id': cls.project.id,
        })
        cls.task = cls.env['project.task'].create({
            'name': 'Task in project 2',
            'project_id': cls.project_2.id,
        })

    def test_01_defaults(self):
        self.assertEqual(self.event.project_id.calculation_type, 'date_end')
        self.assertEqual(self.event.project_id.date,
                         str.split(self.event.date_begin, ' ')[0])
        self.assertEqual(self.event.name, self.event.project_id.name)

    def test_02_project_recalculation(self):
        self.event.date_begin = self.date['begin2']
        self.event.date_end = self.date['end2']
        self.event.name = 'Event name changed'
        self.assertEqual(self.event.project_id.date,
                         str.split(self.event.date_begin, ' ')[0])
        self.assertEqual(self.event.name, self.event.project_id.name)

    def test_03_project_change(self):
        self.event.project_id = self.project_2
        self.assertEqual(self.event.project_id.calculation_type, 'date_end')
        self.assertEqual(self.event.project_id.date,
                         str.split(self.event.date_begin, ' ')[0])
        self.assertEqual(self.event.name, self.event.project_id.name)
        self.assertEqual(self.event.count_tasks, 1)

    def test_04_cancel_and_draft_event(self):
        self.event.button_cancel()
        self.assertFalse(self.event.project_id.active)
        self.event.button_draft()
        self.assertTrue(self.event.project_id.active)
